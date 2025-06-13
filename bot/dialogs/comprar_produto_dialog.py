from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

import requests

class ComprarProdutoDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ComprarProdutoDialog, self).__init__("ComprarProdutoDialog")

        self.add_dialog(TextPrompt("numeroCartaoCreditoPrompt"))
        self.add_dialog(TextPrompt("dataExpiracaoPrompt"))
        self.add_dialog(TextPrompt("cvvPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "comprarProdutoWaterfall",
                [
                    self.numero_cartao_step,
                    self.data_expiracao_step,
                    self.cvv_step,
                    self.final_step
                ],
            )
        )

        self.initial_dialog_id = "comprarProdutoWaterfall"

    async def numero_cartao_step(self, step_context: WaterfallStepContext):
        step_context.values["productId"] = step_context.options.get("productId")

        prompt_message = MessageFactory.text("Por favor, digite o número do seu cartão de crédito:")
        return await step_context.prompt("numeroCartaoCreditoPrompt", PromptOptions(prompt=prompt_message))

    async def data_expiracao_step(self, step_context: WaterfallStepContext):
        step_context.values["numero_cartao"] = step_context.result

        prompt_message = MessageFactory.text("Digite a data de expiração (MM/AAAA):")
        return await step_context.prompt("dataExpiracaoPrompt", PromptOptions(prompt=prompt_message))

    async def cvv_step(self, step_context: WaterfallStepContext):
        step_context.values["data_expiracao"] = step_context.result

        prompt_message = MessageFactory.text("Digite o código de segurança (CVV):")
        return await step_context.prompt("cvvPrompt", PromptOptions(prompt=prompt_message))

    async def final_step(self, step_context: WaterfallStepContext):
        step_context.values["cvv"] = step_context.result

        produto_id = step_context.values["productId"]
        numero_cartao = step_context.values["numero_cartao"]

        pedido_data = {
            "produto_id": produto_id,
            "numero_cartao": numero_cartao
        }

        async def final_step(self, step_context: WaterfallStepContext):
            step_context.values["cvv"] = step_context.result

        produto_id = step_context.values["productId"]
        numero_cartao = step_context.values["numero_cartao"]

        try:
            # 1. Buscar todos os cartões
            cartoes_response = requests.get("http://127.0.0.1:8000/cartoes/")
            if cartoes_response.status_code != 200:
                await step_context.context.send_activity("Erro ao buscar cartões.")
                return await step_context.end_dialog()

            cartoes = cartoes_response.json()
            cartao_encontrado = next((c for c in cartoes if c["numero"] == numero_cartao), None)

            if not cartao_encontrado:
                await step_context.context.send_activity("Cartão não encontrado.")
                return await step_context.end_dialog()

            id_cartao = cartao_encontrado["id_cartao"]

            # 2. Buscar todos os produtos
            produtos_response = requests.get("http://127.0.0.1:8000/produtos/")
            if produtos_response.status_code != 200:
                await step_context.context.send_activity("Erro ao buscar produtos.")
                return await step_context.end_dialog()

            produtos = produtos_response.json()
            produto = next((p for p in produtos if p["id"] == produto_id), None)

            if not produto:
                await step_context.context.send_activity("Produto não encontrado.")
                return await step_context.end_dialog()

            valor = float(produto["preco"])

            # 3. Autorizar a transação
            autorizacao_response = requests.post(
                f"http://127.0.0.1:8000/cartoes/{id_cartao}/autorizacao/",
                json={"valor": valor}
            )

            if autorizacao_response.status_code != 200:
                await step_context.context.send_activity(
                    "Transação negada: saldo insuficiente ou erro na autorização. Pedido não foi registrado."
                )
                return await step_context.end_dialog()

            # 4. Criar o pedido agora que o saldo foi autorizado
            pedido_data = {
                "produto_id": produto_id,
                "numero_cartao": numero_cartao
            }

            pedido_response = requests.post("http://127.0.0.1:8000/pedido/", json=pedido_data)

            if pedido_response.status_code == 201:
                pedido = pedido_response.json()
               
                try:
                    # 5. Buscar saldo atualizado
                    saldo_response = requests.get(f"http://127.0.0.1:8000/cartoes/{id_cartao}/get_saldo/")
                    if saldo_response.status_code == 200:
                        saldo_data = saldo_response.json()
                        saldo_formatado = saldo_data.get("novo_saldo") or saldo_data.get("Saldo")

                        if saldo_formatado is not None:
                            await step_context.context.send_activity(
                                f"\nPedido realizado com sucesso!"
                                f"\nProduto: `{pedido['produto_id']}`"
                                f"\nValor: R$ {pedido['valor']:.2f}"
                                f"\nCartão final: `{pedido['numero_cartao']}`"
                                f"\nNovo saldo disponível: R$ {saldo_formatado:.2f}"
                            )
                            return await step_context.end_dialog()
                except Exception as e:
                    await step_context.context.send_activity(
                        f"Pedido criado, mas não foi possível recuperar o saldo atualizado.\n"
                        f"Erro: {str(e)}"
                    )
                    return await step_context.end_dialog()

                # fallback se saldo não foi retornado
                await step_context.context.send_activity(
                    f"Pedido realizado com sucesso para o produto `{pedido['produto_id']}` "
                    f"no valor de R${pedido['valor']:.2f} com cartão `{pedido['numero_cartao']}`."
                )
            else:
                await step_context.context.send_activity(
                    f"Erro ao registrar o pedido. Código {pedido_response.status_code}: {pedido_response.text}"
                )

        except Exception as e:
            await step_context.context.send_activity(f"Erro ao processar a compra: {str(e)}")

        return await step_context.end_dialog()
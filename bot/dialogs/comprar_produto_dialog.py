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

        try:
            response = requests.post("http://127.0.0.1:8000/pedido/", json=pedido_data)
            if response.status_code == 201:
                pedido = response.json()
                await step_context.context.send_activity(
                    f"Pedido realizado com sucesso para o produto `{pedido['produto_id']}` no valor de R${pedido['valor']} com cartão final `{pedido['numero_cartao']}`."
                )
            else:
                await step_context.context.send_activity(
                    f"Erro ao registrar o pedido. Código {response.status_code}: {response.text}"
                )
        except Exception as e:
            await step_context.context.send_activity(f"Erro ao conectar ao servidor: {str(e)}")

        return await step_context.end_dialog()
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory
import requests

class ExtratoCompraDialog(ComponentDialog):
    def __init__(self):
        super(ExtratoCompraDialog, self).__init__("ExtratoCompraDialog")

        self.add_dialog(TextPrompt("CartaoPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "extratoCompraWaterfall",
                [
                    self.solicitar_cartao_step,
                    self.buscar_extrato_step
                ],
            )
        )

        self.initial_dialog_id = "extratoCompraWaterfall"

    async def solicitar_cartao_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text(
            "Por favor, digite o número do cartão de crédito para consultar o extrato.",
            input_hint=InputHints.expecting_input,
        )
        return await step_context.prompt("CartaoPrompt", PromptOptions(prompt=prompt))

    async def buscar_extrato_step(self, step_context: WaterfallStepContext):
        numero_cartao = step_context.result

        try:
            # 1. Buscar ID do usuário via MySQL (cartao)
            response = requests.get("http://127.0.0.1:8000/cartoes/")
            if response.status_code != 200:
                raise Exception("Erro ao consultar os cartões.")

            cartoes = response.json()
            cartao_encontrado = next((c for c in cartoes if c["numero"] == numero_cartao), None)

            if not cartao_encontrado:
                await step_context.context.send_activity("Cartão não encontrado. Verifique o número digitado.")
                return await step_context.end_dialog()

            id_usuario = str(cartao_encontrado["usuario"])

            # 2. Buscar extrato de pedidos via CosmosDB
            pedidos_response = requests.get(f"http://127.0.0.1:8000/pedidos/usuario/{id_usuario}/")

            if pedidos_response.status_code != 200:
                raise Exception("Erro ao buscar os pedidos.")

            pedidos = pedidos_response.json()

            if not pedidos:
                await step_context.context.send_activity("Nenhum pedido encontrado para este cartão.")
                return await step_context.end_dialog()

            # 3. Montar resposta com resumo dos pedidos
            resposta = "Extrato de Compras:"
            for pedido in pedidos:
                resposta += (
                    f"\nPedido ID: `{pedido['id']}`"
                    f"\nProduto ID: `{pedido['produto_id']}`"
                    f"\nValor: R$ {pedido['valor']:.2f}"
                    f"\nData: {pedido['data_pedido'][:10]}"
                )

            await step_context.context.send_activity(MessageFactory.text(resposta))
            return await step_context.end_dialog()

        except Exception as e:
            await step_context.context.send_activity(f"Erro ao consultar extrato: {str(e)}")
            return await step_context.end_dialog()

# Este dialógo permite ao usuário consultar o extrato de compras associadas a um cartão de crédito.
# Ele solicita o número do cartão, busca o ID do usuário no MySQL e, em seguida, busca o extrato de pedidos no CosmosDB.
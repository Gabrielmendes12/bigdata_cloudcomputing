from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory

import requests

class ConsultarPedidosDialog(ComponentDialog):
    def __init__(self):
        super(ConsultarPedidosDialog, self).__init__("ConsultarPedidosDialog")

        self.add_dialog(TextPrompt("numeroCartaoPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "consultarPedidosWaterfall",
                [self.solicitar_cartao_step, self.exibir_pedidos_step]
            )
        )

        self.initial_dialog_id = "consultarPedidosWaterfall"

    async def solicitar_cartao_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text("Digite o número do cartão que deseja consultar os pedidos:")
        return await step_context.prompt("numeroCartaoPrompt", PromptOptions(prompt=prompt))

    async def exibir_pedidos_step(self, step_context: WaterfallStepContext):
        numero_cartao = step_context.result

        try:
            # 1. Buscar todos os cartões
            response = requests.get("http://127.0.0.1:8000/cartoes/")
            if response.status_code != 200:
                raise Exception("Erro ao consultar os cartões.")

            cartoes = response.json()
            cartao_encontrado = next((c for c in cartoes if c["numero"] == numero_cartao), None)

            if not cartao_encontrado:
                await step_context.context.send_activity("Cartão não encontrado.")
                return await step_context.end_dialog()

            id_usuario = str(cartao_encontrado["usuario"])

            # 2. Consultar pedidos com base no ID do usuário
            pedidos_response = requests.get(f"http://127.0.0.1:8000/pedidos/usuario/{id_usuario}/")

            if pedidos_response.status_code == 200:
                pedidos = pedidos_response.json()
                if not pedidos:
                    await step_context.context.send_activity("Nenhum pedido encontrado para esse cartão.")
                else:
                    mensagem = "Pedidos encontrados:\n"
                    for pedido in pedidos:
                        mensagem += (
                            f"\nProduto: `{pedido['produto_id']}`"
                            f"\nValor: R${pedido['valor']}"
                            f"\nData: {pedido['data_pedido'][:10]}\n"
                        ) 
                    await step_context.context.send_activity(mensagem)
            else:
                await step_context.context.send_activity(f"Erro ao consultar pedidos: {response.status_code}")
        except Exception as e:
            await step_context.context.send_activity(f"Erro de conexão: {str(e)}")

        return await step_context.end_dialog()

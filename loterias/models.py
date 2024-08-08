from typing import Any, Optional

from pydantic import BaseModel, Field


class ListaRateioPremioItem(BaseModel):
    descricao_faixa: str = Field(..., alias='descricaoFaixa')
    faixa: int
    numero_de_ganhadores: int = Field(..., alias='numeroDeGanhadores')
    valor_premio: float = Field(..., alias='valorPremio')


class LotteryDraw(BaseModel):
    id: Any = Field(alias='_id', default=None)
    acumulado: bool
    data_apuracao: str = Field(..., alias='dataApuracao')
    data_proximo_concurso: str = Field(..., alias='dataProximoConcurso')
    dezenas_sorteadas_ordem_sorteio: list[str] = Field(..., alias='dezenasSorteadasOrdemSorteio')
    exibir_detalhamento_por_cidade: bool = Field(..., alias='exibirDetalhamentoPorCidade')
    indicador_concurso_especial: int = Field(..., alias='indicadorConcursoEspecial')
    lista_dezenas: list[str] = Field(..., alias='listaDezenas')
    lista_dezenas_segundo_sorteio: Any = Field(..., alias='listaDezenasSegundoSorteio')
    lista_municipio_uf_ganhadores: list = Field(..., alias='listaMunicipioUFGanhadores')
    lista_rateio_premio: list[ListaRateioPremioItem] = Field(..., alias='listaRateioPremio')
    lista_resultado_equipe_esportiva: Any = Field(..., alias='listaResultadoEquipeEsportiva')
    local_sorteio: str = Field(..., alias='localSorteio')
    municipio_uf_sorteio: str = Field(..., alias='nomeMunicipioUFSorteio')
    time_coracao_mes_sorte: Optional[str] = Field(..., alias='nomeTimeCoracaoMesSorte')
    concurso: int = Field(..., alias='numero')
    concurso_anterior: int = Field(..., alias='numeroConcursoAnterior')
    concurso_final_0_5: int = Field(..., alias='numeroConcursoFinal_0_5')
    concurso_proximo: int = Field(..., alias='numeroConcursoProximo')
    numero_jogo: int = Field(..., alias='numeroJogo')
    observacao: Optional[str]
    premiacao_contingencia: Any = Field(..., alias='premiacaoContingencia')
    tipo_jogo: str = Field(..., alias='tipoJogo')
    tipo_publicacao: int = Field(..., alias='tipoPublicacao')
    ultimo_concurso: bool = Field(..., alias='ultimoConcurso')
    arrecadado: float = Field(..., alias='valorArrecadado')
    acumulado_concurso_0_5: float = Field(..., alias='valorAcumuladoConcurso_0_5')
    acumulado_concurso_especial: float = Field(..., alias='valorAcumuladoConcursoEspecial')
    acumulado_proximo_concurso: float = Field(..., alias='valorAcumuladoProximoConcurso')
    estimado_proximo_concurso: float = Field(..., alias='valorEstimadoProximoConcurso')
    saldo_reserva_garantidora: float = Field(..., alias='valorSaldoReservaGarantidora')
    total_premio_faixa_um: float = Field(..., alias='valorTotalPremioFaixaUm')

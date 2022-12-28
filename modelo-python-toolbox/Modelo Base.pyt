import arcpy
import inspect


parametros_padrao = {
    "name": None,
    "displayName": None,
    "direction": None,
    "datatype": None,
    "parameterType": None,
    "enabled": None,
    "category": None,
    "symbology": None,
    "multiValue": None
}


dict_param_string  = {"direction":"Input", "datatype":"GPString"}
dict_param_feature = {"direction":"Input", "datatype":"GPFeatureLayer"}
dict_param_folder  = {"direction":"Input", "datatype":"DEFolder"}
dict_para_compsto  = {"direction":"Input","datatype":["DERasterDataset", "DERasterCatalog","GPCoordinateSystem"]}


def texto(txt):
    """Recebe uma string e formata ao padrão utf-8"""
    return txt.encode('cp1252')


def textoLista(lista):
    """Recebe uma lista e formata ao padrão utf-8."""
    return [texto(i) for i in lista]


def dicionarioDeParametros(parameters):
    """Retorna { nome_do_parametro : parametro }"""
    dict_params = { p.name:p for p in parameters }
    return dict_params


class CategoriasLayout:

    """Categorias que separam os items dentro da ToolBox"""

    layout = "1. Para Atualizar o Layout"
    outra = texto("2. Outras Informações")

# alguns padroes recorentes usados para o estado do Pará em Regularização Fundiária
class Padroes:

    """Contém a lista com o nome de todos os municípios"""
    
    nomes_municipios = ["abaetetuba","abel figueiredo","acará","afuá","água azul do norte","alenquer","almeirim","altamira","anajás","ananindeua","anapu","augusto corrêa","aurora do pará","aveiro","bagre","baião","bannach","barcarena","belém","belterra","benevides","bom jesus do tocantins","bonito","bragança","brasil novo","brejo grande do araguaia","breu branco","breves","bujaru","cachoeira do arari","cachoeira do piriá","cametá","canaã dos carajás","capanema","capitão poço","castanhal","chaves","colares","conceição do araguaia","concórdia do pará","cumaru do norte","curionópolis","curralinho","curuá","curuçá","dom eliseu","eldorado do carajás","faro","floresta do araguaia","garrafão do norte","goianésia do pará","gurupá","igarapé-açu","igarapé-miri","inhangapi","ipixuna do pará","irituia","itaituba","itupiranga","jacareacanga","jacundá","juruti","limoeiro do ajuru","mãe do rio","magalhães barata","marabá","maracanã","marapanim","marituba","medicilândia","melgaço","mocajuba","moju","mojuí dos campos","monte alegre","muaná","nova esperança do piriá","nova ipixuna","nova timboteua","novo progresso","novo repartimento","óbidos","oeiras do pará","oriximiná","ourém","ourilândia do norte","pacajá","palestina do pará","paragominas","parauapebas","pau d'arco","peixe-boi","piçarra","placas","ponta de pedras","portel","porto de moz","prainha","primavera","quatipuru","redenção","rio maria","rondon do pará","rurópolis","salinópolis","salvaterra","santa bárbara do pará","santa cruz do arari","santa izabel do pará","santa luzia do pará","santa maria das barreiras","santa maria do pará","santana do araguaia","santarém","santarém novo","santo antônio do tauá","são caetano de odivelas","são domingos do araguaia","são domingos do capim","são félix do xingu","são francisco do pará","são geraldo do araguaia","são joão da ponta","são joão de pirabas","são joão do araguaia","são sebastião da boa vista","sapucaia","senador josé porfírio","soure","tailândia","terra alta","terra santa","tomé-açu","tracuateua","trairão","tucumã","tucuruí","ulianópolis","uruará","vigia","viseu","vitória do xingu","xinguara"] 
    municipios = [u'ABAETETUBA',u'ABEL FIGUEIREDO',u'ACAR\xc1',u'AFU\xc1',u'\xc1GUA AZUL DO NORTE',u'ALENQUER',u'ALMEIRIM',u'ALTAMIRA',u'ANAJ\xc1S',u'ANANINDEUA',u'ANAPU',u'AUGUSTO CORR\xcaA',u'AURORA DO PAR\xc1',u'AVEIRO',u'BAGRE',u'BAI\xc3O',u'BANNACH',u'BARCARENA',u'BEL\xc9M',u'BELTERRA',u'BENEVIDES',u'BOM JESUS DO TOCANTINS',u'BONITO',u'BRAGAN\xc7A',u'BRASIL NOVO',u'BREJO GRANDE DO ARAGUAIA',u'BREU BRANCO',u'BREVES',u'BUJARU',u'CACHOEIRA DO PIRI\xc1',u'CACHOEIRA DO ARARI',u'CAMET\xc1',u'CANA\xc3 DOS CARAJ\xc1S',u'CAPANEMA',u'CAPIT\xc3O PO\xc7O',u'CASTANHAL',u'CHAVES',u'COLARES',u'CONCEI\xc7\xc3O DO ARAGUAIA',u'CONC\xd3RDIA DO PAR\xc1',u'CUMARU DO NORTE',u'CURION\xd3POLIS',u'CURRALINHO',u'CURU\xc1',u'CURU\xc7\xc1',u'DOM ELISEU',u'ELDORADO DO CARAJ\xc1S',u'FARO',u'FLORESTA DO ARAGUAIA',u'GARRAF\xc3O DO NORTE',u'GOIAN\xc9SIA DO PAR\xc1',u'GURUP\xc1',u'IGARAP\xc9-A\xc7U',u'IGARAP\xc9-MIRI',u'INHANGAPI',u'IPIXUNA DO PAR\xc1',u'IRITUIA',u'ITAITUBA',u'ITUPIRANGA',u'JACAREACANGA',u'JACUND\xc1',u'JURUTI',u'LIMOEIRO DO AJURU',u'M\xc3E DO RIO',u'MAGALH\xc3ES BARATA',u'MARAB\xc1',u'MARACAN\xc3',u'MARAPANIM',u'MARITUBA',u'MEDICIL\xc2NDIA',u'MELGA\xc7O',u'MOCAJUBA',u'MOJU',u'MOJU\xcd DOS CAMPOS',u'MONTE ALEGRE',u'MUAN\xc1',u'NOVA ESPERAN\xc7A DO PIRI\xc1',u'NOVA IPIXUNA',u'NOVA TIMBOTEUA',u'NOVO PROGRESSO',u'NOVO REPARTIMENTO',u'\xd3BIDOS',u'OEIRAS DO PAR\xc1',u'ORIXIMIN\xc1',u'OUR\xc9M',u'OURIL\xc2NDIA DO NORTE',u'PACAJ\xc1',u'PALESTINA DO PAR\xc1',u'PARAGOMINAS',u'PARAUAPEBAS',u"PAU D'ARCO",u'PEIXE-BOI',u'PI\xc7ARRA',u'PLACAS',u'PONTA DE PEDRAS',u'PORTEL',u'PORTO DE MOZ',u'PRAINHA',u'PRIMAVERA',u'QUATIPURU',u'REDEN\xc7\xc3O',u'RIO MARIA',u'RONDON DO PAR\xc1',u'RUR\xd3POLIS',u'SALIN\xd3POLIS',u'SALVATERRA',u'SANTA B\xc1RBARA DO PAR\xc1',u'SANTA CRUZ DO ARARI',u'SANTA IZABEL DO PAR\xc1',u'SANTA LUZIA DO PAR\xc1',u'SANTA MARIA DAS BARREIRAS',u'SANTA MARIA DO PAR\xc1',u'SANTANA DO ARAGUAIA',u'SANTAR\xc9M',u'SANTAR\xc9M NOVO',u'SANTO ANT\xd4NIO DO TAU\xc1',u'S\xc3O CAETANO DE ODIVELAS',u'S\xc3O DOMINGOS DO ARAGUAIA',u'S\xc3O DOMINGOS DO CAPIM',u'S\xc3O F\xc9LIX DO XINGU',u'S\xc3O FRANCISCO DO PAR\xc1',u'S\xc3O GERALDO DO ARAGUAIA',u'S\xc3O JO\xc3O DA PONTA',u'S\xc3O JO\xc3O DE PIRABAS',u'S\xc3O JO\xc3O DO ARAGUAIA',u'S\xc3O MIGUEL DO GUAM\xc1',u'S\xc3O SEBASTI\xc3O DA BOA VISTA',u'SAPUCAIA',u'SENADOR JOS\xc9 PORF\xcdRIO',u'SOURE',u'TAIL\xc2NDIA',u'TERRA ALTA',u'TERRA SANTA',u'TOM\xc9-A\xc7U',u'TRACUATEUA',u'TRAIR\xc3O',u'TUCUM\xc3',u'TUCURU\xcd',u'ULIAN\xd3POLIS',u'URUAR\xc1',u'VIGIA',u'VISEU',u'VIT\xd3RIA DO XINGU',u'XINGUARA',]
    situacoes = ["REGULARIZAÇÃO NÃO ONEROSA","REGULARIZAÇÃO ONEROSA","PROTOCOLO DE SOLICITAÇÃO DE ACESSO À INFORMAÇÃO","CERTIDÃO", "OUTROS"]
    # TODO IMPLEMENTAR OUTRAS SITUAÇÕES CONFORME O PEDIDO

class Argumentos:

    """Argumentos usados para criar os parametros."""

    checkBoxes   = dict_param_string.update({"category":CategoriasLayout.layout,"multiValue":True})
    stringLayout = dict_param_string.update({"category":CategoriasLayout.layout})
    stringInfo   = dict_param_string.update({"category":CategoriasLayout.outra})
    featureLayer = dict_param_feature
    composto = dict_para_compsto
    string = dict_param_string
    folder = dict_param_folder


class Campos:

    """Definição dos Campos que ficaram dentro da Interface."""

    # Variaveis de Parametros que serão inseridas no Layout
    variavel_parametro = [
        ["Nome do Parametro"]+
        ["key_parametro", "Required"],

        # Tipo de Parametros que ira aparecer no Layout Final
        Argumentos.featureLayer,
    ]


class Constantes:

    def __init__(self):
        self.situacoes = textoLista(Padroes.situacoes)
        self.municipios = textoLista(Padroes.municipios)
        self.argumentos = Argumentos()
        self.categorias_layout = CategoriasLayout()
        self.campos_layout = Campos()


class Parametros:

    """Responsável por recursivamente criar Parametros."""

    def __init__(self):
        self.campos = Campos()
        self.constantes = Constantes()
    
    def getParametros(self):
        """Define recursivamente todos os Parametros baseado nos Campos."""
        return [ arcpy.Parameter(name=j[1],parameterType=j[2],
            displayName=texto(j[0]), **i[1][-1])
                for i in inspect.getmembers(self.campos)
                    if not i[0].startswith("_")
                        for j in i[1] if j != i[1][-1]]

    def setup(self):
        self.prs = self.getParametros()
        return self.prs


class Toolbox(object):
    def __init__(self):
        self.label = "ModeloBase"
        self.alias = "Aqui apenas um exemplo de Base"
        self.tools = [ModeloBase]


class ModeloBase(object):
    def __init__(self):
        self.label = "MeuModeloBase"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        return Parametros().setup()

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        return

import streamlit as st 
from PIL import Image

st.set_page_config( 
                   page_title="Home",
                   page_icon="💵",  layout='wide')

st.title(' Informações de Crédito ')

image=Image.open('images/logo_man.jpg')
st.sidebar.image(image, width=180)
st.sidebar.markdown("## Sistema Financeiro Nacional")
st.sidebar.markdown("##### Dados do Banco Central do Brasil")
st.sidebar.markdown("""---""")
st.sidebar.markdown("""@carlamoema""")
st.markdown ("""
    
O Dashboard foi construído para mostrar o panorama do Mercado de Crédito dentro do Sistema Financeiro Nacional
### Como utilizar esse Dashboard?
    
* Na página Central de Risco, escolha o Tipo de Cliente dentre Pessoa Jurídica e Pessoa Física
* Navegue nas opções dos meses disponíveis:
    - Janeiro
    - Fevereiro        
    - Março
    - Abril
    - Maio
"""      
)

st.markdown ("""

### Algumas premissas foram seguidas para a construção do Dashboard:
    (fonte https://www.bcb.gov.br/content/estabilidadefinanceira/scr/scr.data/scr_data_metodologia.pdf)   

### 1 - Inadimplência:
Calcula-se pela divisão do valor da carteira das operações de crédito com alguma parcela em atraso acima de 90 dias pelo valor da carteira de todas as operações.     

### 2 - Ativo problemático:
Calcula-se pela divisão do valor da carteira das operações de crédito consideradas como Ativos Problemáticos pelo
valor da carteira de todas as operações. 
São consideradas como ativos problemáticos as operações de crédito em atraso há mais de noventa dias e as
operações nas quais existem indícios de que respectiva obrigação não será integralmente honrada. Entende-se que
há indicativos de que a obrigação poderá não ser integralmente honrada, entre outros eventos, quando a operação for objeto de reestruturação e a instituição financeira reconhecer contabilmente deterioração significativa da qualidade do crédito do tomador, classificando-o entre os níveis de risco E e H.        

#### São registrados no SCR:
- empréstimos e financiamentos;
- adiantamentos;
- operações de arrendamento mercantil;
- coobrigações e garantias prestadas;
- compromissos de crédito não canceláveis;
- operações baixadas como prejuízo e créditos contratados com recursos a liberar;
-  demais operações que impliquem risco de crédito;
- operações de crédito que tenham sido objeto de negociação com retenção substancial de riscos e de benefícios ou de controle;
- operações com instrumentos de pagamento pós-pagos; 
- outras operações ou contratos com características de crédito reconhecidas pelo BC.
"""
)

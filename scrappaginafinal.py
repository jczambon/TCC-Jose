import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv
import re
import sys

if __name__ == "__main__":
    bairros_validos = [
    "Centro", "São João do Rio Vermelho", "Itacorubi", "Trindade", "Capoeiras", "Agronômica",
    "Saco dos Limões", "Coqueiros", "Jardim Atlântico", "Córrego Grande", "Tapera da Base",
    "Canasvieiras", "Monte Cristo", "Costeira do Pirajubaé", "Saco Grande", "Estreito",
    "Ingleses do Rio Vermelho", "Abraão", "Pantanal", "Campeche", "Monte Verde",
    "Canto", "João Paulo", "Rio Tavares", "Barra da Lagoa",
    "Balneário", "Vargem do Bom Jesus", "Carianos", "Jurerê Internacional", "Lagoa da Conceição",
    "Santinho", "Vargem Grande", "Coloninha", "Ponta das Canas", "Pântano do Sul",
    "Morro das Pedras", "Alto Ribeirão",
    "Cachoeira do Bom Jesus", "Santo Antônio de Lisboa", "Itaguaçu",
    "Ribeirão da Ilha", "Açores", "Cacupé", "Santa Mônica", "Bom Abrigo",
    "Vargem Pequena", "Canto da Lagoa", "Jurerê", "Carvoeira", "Praia Brava"
    ]
    # Configurar o driver
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(version_main=137, options=options)
    wait = WebDriverWait(driver, 15)

    # Funções auxiliares
    def sleep_random(a=1.5, b=3.0):
        time.sleep(random.uniform(a, b))

    def slow_scroll():
        for _ in range(3):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            sleep_random(0.5, 1.2)

    
    def limpar_numero(texto):
        if not texto:
            return None
        if '-' in texto:
            return None
        numero = re.sub(r'[^\d]', '', texto)
        return int(numero) if numero else None

    def extrair_bairro(texto_raw):
        # Remove prefixos e quebras de linha
        texto = texto_raw.replace('\n', ' ').strip().lower()

        for bairro in bairros_validos:
            if bairro.lower() in texto:
                return bairro  # retorna o nome do bairro original
        return None

    primeira_iteracao = 1
    urls_base = ['https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++jurere/?transacao=venda&onde=,Santa%20Catarina,Florian%C3%B3polis,,Jurer%C3%AA,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EJurere,-27.453544,-48.511221,;,Santa%20Catarina,Florian%C3%B3polis,,Jurer%C3%AA%20Internacional,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EJurere%20Internacional,-27.439982,-48.50105,;,Santa%20Catarina,Florian%C3%B3polis,,Ingleses%20do%20Rio%20Vermelho,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EIngleses%20do%20Rio%20Vermelho,-27.452168,-48.404387,;,Santa%20Catarina,Florian%C3%B3polis,,Ingleses%20Norte,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EIngleses%20Norte,-27.4523,-48.401314,;,Santa%20Catarina,Florian%C3%B3polis,,Praia%20dos%20Ingleses,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EPraia%20dos%20Ingleses,-27.4523,-48.401314,;,Santa%20Catarina,Florian%C3%B3polis,,Ingleses%20Sul,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EIngleses%20Sul,-27.4523,-48.401314,&tipos=apartamento_residencial&',
                 'https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++abraao/?transacao=venda&onde=,Santa%20Catarina,Florian%C3%B3polis,,Abra%C3%A3o,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EAbraao,-27.605795,-48.595048,;,Santa%20Catarina,Florian%C3%B3polis,,Pantanal,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EPantanal,-27.609846,-48.531529,;,Santa%20Catarina,Florian%C3%B3polis,,Monte%20Verde,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EMonte%20Verde,-27.559184,-48.497054,;,Santa%20Catarina,Florian%C3%B3polis,,Canto,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3ECanto,-27.585268,-48.585032,;,Santa%20Catarina,Florian%C3%B3polis,,Joao%20Paulo,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EJoao%20Paulo,-27.559727,-48.511221,;,Santa%20Catarina,Florian%C3%B3polis,,Balne%C3%A1rio,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EBalneario,-27.579533,-48.582528,;,Santa%20Catarina,Florian%C3%B3polis,,Vargem%20do%20Bom%20Jesus,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EVargem%20do%20Bom%20Jesus,-27.442069,-48.426274,;,Santa%20Catarina,Florian%C3%B3polis,,Carianos,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3ECarianos,-27.662146,-48.537482,;,Santa%20Catarina,Florian%C3%B3polis,,Barra%20da%20Lagoa,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EBarra%20da%20Lagoa,-27.574089,-48.431267,;,Santa%20Catarina,Florian%C3%B3polis,,Lagoa,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3ELagoa,-27.603092,-48.47123,;,Santa%20Catarina,Florian%C3%B3polis,,Santinho,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3ESantinho,-27.4523,-48.401314,;,Santa%20Catarina,Florian%C3%B3polis,,Vargem%20Grande,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EVargem%20Grande,-27.455797,-48.447498,;,Santa%20Catarina,Florian%C3%B3polis,,Coloninha,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EColoninha,-27.590402,-48.592544,&tipos=apartamento_residencial&',
                 'https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++estreito/?transacao=venda&onde=,Santa%20Catarina,Florian%C3%B3polis,,Estreito,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EEstreito,-27.592206,-48.577521,;,Santa%20Catarina,Florian%C3%B3polis,,Agron%C3%B4mica,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EAgronomica,-27.578449,-48.536231,;,Santa%20Catarina,Florian%C3%B3polis,,Itacorubi,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EItacorubi,-27.580226,-48.504667,;,Santa%20Catarina,Florian%C3%B3polis,,Trindade,,,neighborhood,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3ETrindade,-27.590339,-48.512472,&tipos=apartamento_residencial&',
                 'https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++centro/?transacao=venda&onde=,Santa%20Catarina,Florianópolis,,Centro,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Centro,-27.592269,-48.549027,;,Santa%20Catarina,Florianópolis,,Capoeiras,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Capoeiras,-27.598399,-48.591291,&tipos=apartamento_residencial&',
                 'https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++saco-dos-limoes/?transacao=venda&onde=,Santa%20Catarina,Florianópolis,,Saco%20dos%20Limões,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Saco%20dos%20Limoes,-27.609846,-48.531529,;,Santa%20Catarina,Florianópolis,,Coqueiros,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Coqueiros,-27.607956,-48.581662,;,Santa%20Catarina,Florianópolis,,Jardim%20Atlântico,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Jardim%20Atlantico,-27.580896,-48.5963,;,Santa%20Catarina,Florianópolis,,Córrego%20Grande,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Corrego%20Grande,-27.593609,-48.502741,;,Santa%20Catarina,Florianópolis,,Tapera%20da%20Base,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Tapera%20da%20Base,-27.688876,-48.561252,;,Santa%20Catarina,Florianópolis,,Canasvieiras,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Canasvieiras,-27.432258,-48.458212,;,Santa%20Catarina,Florianópolis,,Monte%20Cristo,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Monte%20Cristo,-27.590706,-48.600056,;,Santa%20Catarina,Florianópolis,,Costeira%20do%20Pirajubaé,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Costeira%20do%20Pirajubae,-27.634992,-48.521946,;,Santa%20Catarina,Florianópolis,,Saco%20Grande,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Saco%20Grande,-27.540117,-48.503721,;,Santa%20Catarina,Florianópolis,,Estreito,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Estreito,-27.592206,-48.577521,&tipos=apartamento_residencial&',
                 'https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++s-joao-do-rio-vermelho/?transacao=venda&onde=,Santa%20Catarina,Florianópolis,,São%20João%20do%20Rio%20Vermelho,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Sao%20Joao%20do%20Rio%20Vermelho,-27.491002,-48.419866,;,Santa%20Catarina,Florianópolis,,Campeche,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Campeche,-27.596858,-48.546812,;,Santa%20Catarina,Florianópolis,,Rio%20Tavares,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Rio%20Tavares,-27.645743,-48.472479,;,Santa%20Catarina,Florianópolis,,Lagoa%20da%20Conceição,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Lagoa%20da%20Conceicao,-27.603092,-48.47123,;,Santa%20Catarina,Florianópolis,,Ponta%20das%20Canas,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Ponta%20das%20Canas,-27.413127,-48.426274,;,Santa%20Catarina,Florianópolis,,Pântano%20do%20Sul,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Pantano%20do%20Sul,-27.779766,-48.507974,;,Santa%20Catarina,Florianópolis,,Morro%20das%20Pedras,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Morro%20das%20Pedras,-27.709706,-48.502471,;,Santa%20Catarina,Florianópolis,,Alto%20Ribeirão,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Alto%20Ribeirao,-27.809901,-48.560435,;,Santa%20Catarina,Florianópolis,,Cachoeira%20do%20Bom%20Jesus,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Cachoeira%20do%20Bom%20Jesus,-27.43122,-48.436261,;,Santa%20Catarina,Florianópolis,,Santo%20Antônio%20de%20Lisboa,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Santo%20Antonio%20de%20Lisboa,-27.50636,-48.519989,;,Santa%20Catarina,Florianópolis,,Itaguaçu,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Itaguacu,-27.605795,-48.595048,;,Santa%20Catarina,Florianópolis,,Ribeirão%20da%20Ilha,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Ribeirao%20da%20Ilha,-27.809901,-48.560435,;,Santa%20Catarina,Florianópolis,,Açores,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Acores,-27.779766,-48.507974,;,Santa%20Catarina,Florianópolis,,Cacupé,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Cacupe,-27.536963,-48.524975,;,Santa%20Catarina,Florianópolis,,Santa%20Mônica,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Santa%20Monica,-27.593609,-48.502741,;,Santa%20Catarina,Florianópolis,,Bom%20Abrigo,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Bom%20Abrigo,-27.611454,-48.595674,;,Santa%20Catarina,Florianópolis,,Vargem%20Pequena,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Vargem%20Pequena,-27.472388,-48.459987,;,Santa%20Catarina,Florianópolis,,Canto%20da%20Lagoa,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Canto%20da%20Lagoa,-27.603092,-48.47123,;,Santa%20Catarina,Florianópolis,,Carvoeira,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Carvoeira,-27.603775,-48.526226,;,Santa%20Catarina,Florianópolis,,Praia%20Brava,,,neighborhood,BR>Santa%20Catarina>NULL>Florianopolis>Barrios>Praia%20Brava,-27.403024,-48.41504,&tipos=apartamento_residencial&']

    for url_base in urls_base:
        pagina_atual = 1

        driver.get(url_base)
        sleep_random(2, 4)

        data = []
        visited = set()

        try:
            while True:
                anuncios = driver.find_elements(By.CSS_SELECTOR, 'li[data-cy="rp-property-cd"] a')
                anuncios = [a for a in anuncios if a.get_attribute('href') not in visited and a.get_attribute('href')]

                # Se não houver anúncios novos, tentar próxima página
                if not anuncios:
                    # Salvar dados parciais
                    if data:
                        with open('imoveisfinal.csv', 'a', newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=['preco', 'bairro', 'area', 'quartos', 'suites', 'vagas', 'andar', 'banheiros',
                                                                'salao de festas', 'mobiliado', 'varanda', 'academia', 'espaco gourmet',
                                                                'playground', 'churrasqueira', 'piscina'])
                            if primeira_iteracao == 1:
                                writer.writeheader()
                            writer.writerows(data)
                        data = []

                    pagina_atual += 1
                    primeira_iteracao = 0
                    next_url = f'{url_base}pagina={pagina_atual}'
                    driver.get(next_url)
                    sleep_random(2, 4)

                    anuncios = driver.find_elements(By.CSS_SELECTOR, 'li[data-cy="rp-property-cd"] a')
                    anuncios = [a for a in anuncios if a.get_attribute('href') not in visited]

                    if not anuncios:
                        print("Não há mais anúncios. Finalizando...")
                        break

                for anuncio in anuncios:
                    try:
                        link = anuncio.get_attribute('href')
                        if not link or link in visited:
                            continue

                        visited.add(link)


                        bairro_element = anuncio.find_element(By.CSS_SELECTOR, 'h2[data-cy="rp-cardProperty-location-txt"]')
                        bairro_raw = bairro_element.text
                        bairro = extrair_bairro(bairro_raw)


                        # Simular movimento até o anúncio antes de clicar
                        ActionChains(driver).move_to_element(anuncio).pause(random.uniform(0.5, 1.5)).click(anuncio).perform()
                        sleep_random(2, 4)

                        driver.switch_to.window(driver.window_handles[1])

                        # Extrair os dados atualizados
                        try:
                            preco = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="price-info-value"]'))).text
                        except:
                            preco = None

                        try:
                            detalhes = driver.find_elements(By.CSS_SELECTOR, 'ul.amenities-list li')
                            area = andar = None
                            suites = vagas = quartos = banheiro = salao_de_festas = mobiliado = varanda = academia = espaco_gourmet = playground = churrasqueira = piscina = 0
                            for d in detalhes:
                                texto = d.get_attribute("textContent").strip().lower()
                                if 'm²' in texto:
                                    area = limpar_numero(texto)
                                elif 'quarto' in texto:
                                    quartos = limpar_numero(texto)
                                elif 'suíte' in texto:
                                    suites = limpar_numero(texto)
                                elif 'vaga' in texto:
                                    vagas = limpar_numero(texto)
                                elif 'andar' in texto:
                                    andar = limpar_numero(texto)
                                elif 'banheiro' in texto:
                                    banheiro = limpar_numero(texto)
                                elif 'salão de festas' in texto:
                                    salao_de_festas = 1
                                elif 'mobiliado' in texto:
                                    mobiliado = 1
                                elif 'varanda' in texto:
                                    varanda = 1
                                elif 'academia' in texto:
                                    academia = 1
                                elif 'espaço gourmet' in texto:
                                    espaco_gourmet = 1
                                elif 'playground' in texto:
                                    playground = 1
                                elif 'churrasqueira' in texto:
                                    churrasqueira = 1
                                elif 'piscina' in texto:
                                    piscina = 1
                        except:
                            area = quartos = suites = vagas = andar = banheiro = salao_de_festas = mobiliado = varanda = academia = espaco_gourmet = playground = churrasqueira = piscina = None

                        data.append({
                            'preco': preco,
                            'bairro': bairro,
                            'area': area,
                            'quartos': quartos,
                            'suites': suites,
                            'vagas': vagas,
                            'andar': andar,
                            'banheiros': banheiro,
                            'salao de festas': salao_de_festas,
                            'mobiliado': mobiliado,
                            'varanda': varanda,
                            'academia': academia,
                            'espaco gourmet': espaco_gourmet,
                            'playground': playground,
                            'churrasqueira': churrasqueira,
                            'piscina': piscina
                        })

                        print(data[-1])

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        sleep_random(1, 2)
                    except Exception as e:
                        print(f"Erro: {e}")
                        if len(driver.window_handles) > 1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        continue

                slow_scroll()

        except KeyboardInterrupt:
            driver.quit()
            sys.exit()
    driver.quit()
    print("Código finalizado")
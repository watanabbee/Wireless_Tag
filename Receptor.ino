#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <WifiUDP.h>
#include <Wire.h>
#include <SSD1306.h>

const char *ssid = "Net-Virtua-7762-2.4G";
const char *password = "3743477620";
const int serverPort = 80;

WiFiUDP ntpUDP;
SSD1306  display(0x3c, 0, 2);

ESP8266WebServer server(serverPort);

void setup() {
  Serial.begin(115200);
  delay(10);
  Wire.pins(0, 2);
  Wire.begin(0, 2);
  display.init();
  display.flipScreenVertically();

  display.drawString(0, 10, "Conectando ao WiFi...");
  display.display();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");

  }
  display.drawString(0, 24, "Conectado.");
  display.display();
  Serial.println("Conectado ao WiFi com sucesso!");
  Serial.print("Endereço IP do servidor: ");
  Serial.println(WiFi.localIP());
  Serial.println("Esperando dados da Bridge...");

  server.on("/receber_dados", HTTP_POST, [](){
    String dados = server.arg("plain");
    Serial.println("Dados recebidos: " + dados);
    
    mostrarDadosNoDisplay(dados);
    
    server.send(200, "text/plain", "Dados recebidos com sucesso!");
  });

  server.begin();

  delay(1000);
}

void loop() {
  server.handleClient();
 }

void mostrarDadosNoDisplay(String dados) {
  display.clear();
  display.setTextAlignment(TEXT_ALIGN_CENTER);
  display.setFont(ArialMT_Plain_16);

  int posDoisPontosNome = dados.indexOf(':') + 3; 
  int posDoisPontosPreco = dados.lastIndexOf(':') + 3; 

  String nomeProduto = dados.substring(posDoisPontosNome, dados.indexOf('"', posDoisPontosNome));
  String precoProduto = dados.substring(posDoisPontosPreco, dados.indexOf('"', posDoisPontosPreco));

  display.drawString(64, 8, nomeProduto);
  Serial.print("nome do produto: ");
  Serial.println(nomeProduto);

  display.setFont(ArialMT_Plain_16); 
  display.drawString(64, 36, precoProduto);
  Serial.print("valor do produto: ");
  Serial.println(precoProduto);

  display.display();

}


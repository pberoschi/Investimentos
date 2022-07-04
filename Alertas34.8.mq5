//+------------------------------------------------------------------+
//|                                                  EA_Telegram.mq5 |
//|                                          Copyright 2020, CMTrade |
//|                                     https://www.fenerickmql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, CMTrade"
#property link      "https://www.fenerickmql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| INCLUDES                                                         |
//+------------------------------------------------------------------+
#include <Telegram.mqh>
#include <Trade/Trade.mqh> // biblioteca-padrão CTrade
CCustomBot bot;
//+------------------------------------------------------------------+
//| INPUTS                                                           |
//+------------------------------------------------------------------+
input int lote = 1;
input int periodoCurta = 8;
input int periodoLonga = 34;
//input string Token = ""; // Chave do bot
//input float Preco = ""; // Preco
//+------------------------------------------------------------------+
//| GLOBAIS                                                          |
//+------------------------------------------------------------------+
//--- manipuladores dos indicadores de média móvel
int curtaHandle = INVALID_HANDLE;
int longaHandle = INVALID_HANDLE;
//--- vetores de dados dos indicadores de média móvel
double mediaCurta[];
double mediaLonga[];
//--- declarara variável trade
CTrade trade;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
  
  //---
   ArraySetAsSeries(mediaCurta,true);
   ArraySetAsSeries(mediaLonga,true);

//--- atribuir p/ os manipuladores de média móvel
   curtaHandle = iMA(_Symbol,_Period,periodoCurta,0,MODE_EMA,PRICE_CLOSE);
   longaHandle = iMA(_Symbol,_Period,periodoLonga,0,MODE_EMA,PRICE_CLOSE);
   
//--- create timer
   EventSetTimer(5);
   
   bot.Token("1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I");
   if(bot.GetMe()!=0)
     {
      Print("Erro na inicialização do bot");
      return INIT_FAILED;
     }
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   if(isNewBar())
     {
      // execute a lógica operacional do robô  
      //+------------------------------------------------------------------+
      //| OBTENÇÃO DOS DADOS                                               |
      //+------------------------------------------------------------------+
      int copied1 = CopyBuffer(curtaHandle,0,0,3,mediaCurta);
      int copied2 = CopyBuffer(longaHandle,0,0,3,mediaLonga);
      //---
      bool sinalCompra = false;
      bool sinalVenda = false;
      //--- se os dados tiverem sido copiados corretamente
      if(copied1==3 && copied2==3)
        {
         //--- sinal de compra
         if( mediaCurta[1]>mediaLonga[1] && mediaCurta[2]<mediaLonga[2] )
           {
            sinalCompra = true;
            bot.GetUpdates(); // Obter mensagens
            bot.SendMessage(-351556985,"Sinal de COMPRA para o " + _Symbol + " 8R");
           }
         //--- sinal de venda
         if( mediaCurta[1]<mediaLonga[1] && mediaCurta[2]>mediaLonga[2] )
           {
            sinalVenda = true;
            bot.GetUpdates(); // Obter mensagens
            bot.SendMessage(-351556985,"Sinal de VENDA para o " + _Symbol + " 8R");
           }
        }
     }
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool isNewBar()
  {
//--- memorize the time of opening of the last bar in the static variable
   static datetime last_time=0;
//--- current time
   datetime lastbar_time=(datetime)SeriesInfoInteger(Symbol(),Period(),SERIES_LASTBAR_DATE);

//--- if it is the first call of the function
   if(last_time==0)
     {
      //--- set the time and exit
      last_time=lastbar_time;
      return(false);
     }

//--- if the time differs
   if(last_time!=lastbar_time)
     {
      //--- memorize the time and return true
      last_time=lastbar_time;
      return(true);
     }
//--- if we passed to this line, then the bar is not new; return false
   return(false);
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
  }
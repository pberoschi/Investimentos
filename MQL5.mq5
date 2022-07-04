//+------------------------------------------------------------------+
//|                                                   Rompimento.mq5 |
//|                                  Copyright 2021, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>

CTrade DayTrade;

input string Inicio = "09:16";
input string Termino = "10:00";
input string Fechamento = "16:00";

//Armazenar data e hora
MqlDateTime horario_inicio, horario_termino, horario_fechamento, horario_atual, dia;

bool operacao_diaria = false;
int contarCandle = 0;
int barraOperacao = 0;

int OnInit(){

   //conversao para mql
   TimeToStruct(StringToTime(Inicio), horario_inicio);
   TimeToStruct(StringToTime(Termino), horario_termino);
   TimeToStruct(StringToTime(Fechamento), horario_fechamento);
   
   if(horario_inicio.hour > horario_termino.hour || (horario_inicio.hour == horario_termino.hour && horario_inicio.min > horario_termino.min)){
      printf("Parâmetros de entrada inválidos!");
      return INIT_FAILED;
   }
   if(horario_termino.hour > horario_fechamento.hour || (horario_termino.hour == horario_fechamento.hour && horario_termino.min > horario_fechamento.min)){
      printf("Parâmetros de entrada inválidos!");
      return INIT_FAILED;
   }
   return INIT_SUCCEEDED;
      
   EventSetTimer(60);
   

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
   //Obter ultimo valor negociado
   MqlTick ultimoTick;
   SymbolInfoTick(_Symbol,ultimoTick);
   
   if(HorarioFechamento()){
      operacao_diaria = false;
      contarCandle = 0;
      barraOperacao = 0;  
   }
   
   
   // Contar Candles
   MqlRates preco[];
   ArraySetAsSeries(preco,true);
   CopyRates(_Symbol,PERIOD_CURRENT,0,3,preco);
   static datetime ultimaVerificacaoTempo;
   datetime tempoCandleCorrente;
   tempoCandleCorrente = preco[0].time;
   if(tempoCandleCorrente != ultimaVerificacaoTempo){
      ultimaVerificacaoTempo = tempoCandleCorrente;
      contarCandle++;
      //
   }
   
   //Ordem de compra
   if(PositionsTotal()==0 && ultimoTick.last > iHigh(_Symbol,PERIOD_CURRENT,1) && HorarioEntrada() == true
      && contarCandle > barraOperacao){
      double stopLoss = NormalizarPreco(iLow(_Symbol,PERIOD_CURRENT,1));
      DayTrade.Buy(1,_Symbol,ultimoTick.last,stopLoss,ultimoTick.last+10);
      operacao_diaria == true;
      barraOperacao = contarCandle;   
   }  
   
   //Ordem de venda
   if(PositionsTotal()==0 && ultimoTick.last > iLow(_Symbol,PERIOD_CURRENT,1) && HorarioEntrada() == true
   && contarCandle > barraOperacao){
      operacao_diaria == false && HorarioEntrada() == true){
      double stopLoss = NormalizarPreco(iHigh(_Symbol,PERIOD_CURRENT,1));
      DayTrade.Sell(1,_Symbol,ultimoTick.last,stopLoss,ultimoTick.last-10);  
      operacao_diaria == true;    
   }    

   }

bool HorarioEntrada()
      {
       TimeToStruct(TimeCurrent(),horario_atual);
       
      if(horario_atual.hour >= horario_inicio.hour && horario_atual.hour <= horario_termino.hour){
      // hora atual igual a de inicio
      if (horario_atual.hour == horario_inicio.hour)
         // Se minuto atual maior ou igual ao de inicio => está no horário de entradas
         if(horario_atual.min >= horario_inicio.min)
            return true;
            // do contrário não está no horário de entradas
         else
            return false;
      
      // hora atual igual a de término
      if(horario_atual.hour == horario_termino.hour)
         //Se minuto atul menor ou igua ao de termino => está no horário de entradas
         if(horario_atual.min <= horario_termino.min)
            return true;
         // do contrário não está no horario de entradas
         else
            return false;
            
      // hora atual maior do que a de inicio e menor que a de termino
      return true;
   }
      
   // hora fora do horario de entradas
   return false;
}


bool HorarioFechamento(){
   TimeToStruct(TimeCurrent(),horario_atual);
   
   // hora dentro do horario de fechamento
   if(horario_atual.hour >= horario_fechamento.hour){
      // hora atual igual a de fechamento
      if(horario_atual.hour == horario_fechamento.hour)
         // se minuto atual maior ou igual ao de fechamento => esta no horario de fechamento
        if(horario_atual.min >= horario_fechamento.min)
           return true;
            // do contrario não esta no horario de fechamento
         else
            return false;

      // hora atual maior que a de fechamento
      return true;
   }
   
   // hora fora do horario de fechamento
   return false;
   }

//Função normalizadora
double NormalizarPreco(double preco){
   //Pegar o tamanho do tick
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

   if(tickSize == 0.0){
      return (NormalizeDouble(preco,_Digits));
   }
   
   return(NormalizeDouble(MathRound(preco/tickSize)*tickSize,_Digits));
   
   
   
}
   
   }

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
  {
//---
   
   }
   
   
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)

   {
//---
   
   }

//+------------------------------------------------------------------+

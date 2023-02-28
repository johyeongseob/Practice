#include "LedControl.h" //install LedControl library

LedControl dot = LedControl(12,11,10,1);
//(din, clk, cs, 매트릭스 개수) 설정

byte heart[] ={
  B01000010,
  B11100111,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00011000
}; //하트모양 배열



void setup() {
  dot.shutdown(0, false); //'절전모드 false' 설정
  dot.setlntensity(0,5); //밝기 조절
  dot.clearDisplay(0); //초기화 설정

}

void loop() {
  dotmatrix(0); //0의 값 가짐 
}

void dotmatrix(int a){
  if (a==0) {
    for (int i = 0; i<8; 1++)
    {
      dot.setRow(0, i, heart[i]);
    }
  }
}

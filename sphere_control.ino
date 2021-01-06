#define M12_CW 2
#define M12_CCW 3
#define PWM12 4

#define M3_CW 7
#define M3_CCW 8
#define PWM3 5

#define M4_CW 9
#define M4_CCW 10
#define PWM4 6

String command="";
int dist=55;
//int dists=20;
int loopl=156;
int mpos=0;
int mpos1=0;
int mpos2=0;
int range=5;
int mdelay=50;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(M12_CW,OUTPUT);
  pinMode(M12_CCW,OUTPUT);
  pinMode(M3_CW,OUTPUT);
  pinMode(M3_CCW,OUTPUT);
  pinMode(M4_CW,OUTPUT);
  pinMode(M4_CCW,OUTPUT);
  pinMode(PWM12,OUTPUT);
  pinMode(PWM3,OUTPUT);
  pinMode(PWM4,OUTPUT);

}
void turn1m1(int k=1){
    digitalWrite(M3_CW, HIGH);
    digitalWrite(M3_CCW, LOW);
    analogWrite(PWM3, 150);
    delay(dist*k);
    digitalWrite(M3_CW, LOW);
    analogWrite(PWM3, LOW);
    mpos1+=k;
}
void turn1m2(int k=1){
    digitalWrite(M4_CW, LOW);
    digitalWrite(M4_CCW, HIGH);
    analogWrite(PWM4, 150);
    delay(dist*k);
    digitalWrite(M4_CCW, LOW);
    analogWrite(PWM4, LOW);
    mpos2+=k;
}
void turn2m1(int k=1){
    digitalWrite(M3_CW, LOW);
    digitalWrite(M3_CCW, HIGH);
    analogWrite(PWM3, 150);
    delay(dist*k);
    digitalWrite(M3_CCW, LOW);
    analogWrite(PWM3, LOW);
    mpos1-=k;
}
void turn2m2(int k=1){
    digitalWrite(M4_CW, HIGH);
    digitalWrite(M4_CCW, LOW);
    analogWrite(PWM4, 150);
    delay(dist*k);
    digitalWrite(M4_CW, LOW);
    analogWrite(PWM4, LOW);
    mpos2-=k;
}
void turn1(int k=1){
    digitalWrite(M3_CW, HIGH);
    digitalWrite(M3_CCW, LOW);
    digitalWrite(M4_CCW, HIGH);
    digitalWrite(M4_CW, LOW);
    analogWrite(PWM3, 150);
    analogWrite(PWM4, 150);
    delay(dist*k);
    digitalWrite(M3_CW, LOW);
    digitalWrite(M4_CCW, LOW);
    analogWrite(PWM3, LOW);
    analogWrite(PWM4, LOW);
    if (mpos1<range and mpos1>-range){
      mpos1+=k;
    }
    if (mpos2<range and mpos2>-range){
      mpos1+=k;
    }
}
void turn2(int k=1){
    digitalWrite(M3_CW, LOW);
    digitalWrite(M3_CCW, HIGH);
    digitalWrite(M4_CCW, LOW);
    digitalWrite(M4_CW, HIGH);
    analogWrite(PWM3, 150);
    analogWrite(PWM4, 150);
    delay(dist*k);
    digitalWrite(M3_CCW, LOW);
    digitalWrite(M4_CW, LOW);
    analogWrite(PWM3, LOW);
    analogWrite(PWM4, LOW);
    if (mpos1<range and mpos1>-range){
      mpos1-=k;
    }
    if (mpos2<range and mpos2>-range){
      mpos1-=k;
    }
}
void center(){
  if (mpos1==mpos2){
    if (mpos1<0){
      mpos1*=-1;
      turn1(mpos1);
      mpos1=0;
      mpos2=0;
    }
    else if (mpos1>0)
    {
      turn2(mpos1);
      mpos1=0;
      mpos2=0;
    }
  } else{
    if (mpos1<0){
      mpos1*=-1;
      turn1m1(mpos1);
      mpos1=0;
    }
    else if (mpos1>0)
    {
      turn2m1(mpos1);
      mpos1=0;
    }
    if (mpos2<0){
      mpos2*=-1;
      turn1m2(mpos2);
      mpos2=0;
    }
    else if (mpos2>0)
    {
      turn2m2(mpos2);
      mpos2=0;
    }
  }
}
void Stop(){
  digitalWrite(M12_CW, LOW);
  digitalWrite(M12_CCW, LOW);
  analogWrite(PWM12, LOW);
  center();
}
void forward(){
  int i=0;
  while(i<loopl){
    digitalWrite(M12_CW, HIGH);
    digitalWrite(M12_CCW, LOW);
    analogWrite(PWM12, 150);
    delay(mdelay);
    digitalWrite(M12_CW, LOW);
    digitalWrite(M12_CCW, LOW);
    delay(mdelay);
    i++;
  }
  delay(2*mdelay);
  digitalWrite(M12_CW, HIGH);
  analogWrite(PWM12, 150);
  delay(mdelay);
    digitalWrite(M12_CW, LOW);
    digitalWrite(M12_CCW, LOW);
  analogWrite(PWM12, LOW);
  i=0;
}
void backward(){
  int i=0;
  while(i<loopl){
    digitalWrite(M12_CW, LOW);
    digitalWrite(M12_CCW, HIGH);
    analogWrite(PWM12, 150);
    delay(mdelay);
    digitalWrite(M12_CW, LOW);
    digitalWrite(M12_CCW, LOW);
    delay(mdelay);
    i++;
  }
  delay(2*mdelay);
  digitalWrite(M12_CW, LOW);
  digitalWrite(M12_CCW, HIGH);
  delay(mdelay);
  digitalWrite(M12_CW, LOW);
  digitalWrite(M12_CCW, LOW);
  analogWrite(PWM12, LOW);
  i=0;
}

void rotate1(){
  center();
  delay(100);
  digitalWrite(M3_CW, HIGH);
  digitalWrite(M3_CCW, LOW);
  digitalWrite(M4_CW, HIGH);
  digitalWrite(M4_CCW, LOW);
  analogWrite(PWM3, 150);
  analogWrite(PWM4, 150);
  delay(range*dist);
  digitalWrite(M3_CW, LOW);
  digitalWrite(M4_CW, LOW);
  analogWrite(PWM3, LOW);
  analogWrite(PWM4, LOW);
  mpos1=range;
  mpos2=-range;
  /*int m1_diff=range-mpos1;
  int m2_diff=-range-mpos2;
  if (m2_diff<0){
    m2_diff*=-1;
  }
  turn1m1(m1_diff);
  turn2m2(m2_diff);*/
}
void rotate2(){
  center();
  delay(100);
  digitalWrite(M3_CW, LOW);
  digitalWrite(M3_CCW, HIGH);
  digitalWrite(M4_CW, LOW);
  digitalWrite(M4_CCW, HIGH);
  analogWrite(PWM3, 150);
  analogWrite(PWM4, 150);
  delay(range*dist);
  digitalWrite(M3_CW, LOW);
  digitalWrite(M4_CW, LOW);
  analogWrite(PWM3, LOW);
  analogWrite(PWM4, LOW);
  mpos1=-range;
  mpos2=range;
  /*int m1_diff=-range-mpos1;
  int m2_diff=range-mpos2;
  if (m1_diff<0){
    m1_diff*=-1;
  }
  turn2m1(m1_diff);
  turn1m2(m2_diff);*/
}
void halft1(){
  int half=range/2;
  center();
  turn1(half);
  mpos1=half;
  mpos2=half;
}
void halft2(){
  int half=range/2;
  center();
  turn2(half);
  mpos1=-half;
  mpos2=-half;
}
void loop() {
  command="";
  if (Serial.available()){
    command = Serial.readStringUntil('\n');
    //Serial.write(command);
  }
  if (isDigit(command[0])){
    loopl=command.toInt();
  }
  else{
    switch(command[0]){
    case 'r':
      backward();
      break;
    case 'f':
      forward();
      break;
    case 's':
      backward();
      break;
    case 'w':
      forward();
      break;
    /*case 'a':
      turn1();
      break;
    case 'd':
      turn2();
      break;
    case 'l':
      loopl-=2;
      if(loopl<2){
        loopl=2;
      }
      break;
    case 'k':
      loopl+=2;
      break;*/
    case 'c':
      center();
      break;
    case 'e':
      rotate1();
      break;
    case 'q':
      rotate2();
      break;
    case 'x':
      halft1();
      break;
    case 'v':
      halft2();
      break;
    case '4':
      range=4;
      break;
    case '5':
      range=5;
      break;
    case 'o':
      mdelay-=25;
      if(mdelay<25){
        mdelay=25;
      }
      break;
    case 'p':
      mdelay+=25;
      break;
    case 'h':
      dist-=5;
      if (dist<5){
        dist=5;
      }
      break;
    case 'j':
      dist+=5;
      break;
  }
  }
  
}
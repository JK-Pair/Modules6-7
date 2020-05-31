#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8 MHz, clock = 32MHz)
#PIN_SELECT U1RX = PIN_B12 //PIN_B14 //
#PIN_SELECT U1TX = PIN_B13 //PIN_B15 //
#use rs232 (UART1, BAUD = 115200, XMIT = PIN_B13, RCV = PIN_B12)


#define TIME_PERIOD 2000
#define tolerance 30

#define servoTop   PIN_B8 
#define	servoUnder  PIN_B15

#define	lim_SW_X PIN_B14
#define lim_SW_Y PIN_B4
#define lim_SW_Z PIN_B5

#define motorXI  PIN_B0 
#define motorXII PIN_B1
#define ena_X    PIN_B2 
//Encoder X is INT0 PIN_B7

#define	motorYI  PIN_A2
#define motorYII PIN_A4
#define ena_Y    PIN_B9
#define	encodeY  PIN_B6

#define	motorZI  PIN_A0 
#define motorZII PIN_A1 
#define ena_Z    PIN_B10
#define	encodeZ  PIN_B3


#PIN_SELECT INT1 = encodeY 
#PIN_SELECT INT2 = encodeZ 
#PIN_SELECT OC1 =  ena_X  
#PIN_SELECT OC2 =  ena_Y
#PIN_SELECT OC3 =  ena_Z
#PIN_SELECT OC4 =  servoTop
#PIN_SELECT OC5 =  servoUnder

int countX = 0;
int countY = 0;
int countZ = 0; 

char arrayData[6] = {};
char arrayDataXI[2] = {};
char arrayDataXII[2] = {};
char arrayDataYI[2] = {};
char arrayDataYII[2] = {};
char arrayAng[2] = {};
char arrayAngGrip[2] = {};

char SM_id = 1;
int getPackage = 0;
void SM_RxD(int c){
	if (SM_id <= 2){
		if (c ==  0xFF){
			SM_id++;
		}else{
			SM_id = 1;
		}
	}else if (SM_id <= 3){
		if (c == 0x02){
			SM_id++;
		}else{
			SM_id = 1;
		}
	}else if (SM_id <= 4){
		if ( c == 0x06){
			SM_id++;
		}else{
			SM_id = 1;
		}
	}else if (SM_id > 4 && SM_id <= 6){
		arrayDataXI[SM_id - 5] = c; //PosX
		SM_id++;
	}else if (SM_id == 7){
		arrayData[SM_id - 7] = c;	//DirPosX[0]
		SM_id++;
	}else if (SM_id > 7 && SM_id <= 9){
		arrayDataYI[SM_id - 8] = c;	//PosY
		SM_id++;
	}else if (SM_id == 10){
		arrayData[SM_id - 9] = c;	//DirPosY[1]
		SM_id++;
	}else if (SM_id > 10 && SM_id <= 12){
		arrayAng[SM_id - 11] = c;	//Ang
		SM_id++;
	}else if (SM_id > 12 && SM_id <= 14){
		arrayDataXII[SM_id - 13] = c;//goX
		SM_id++;
	}else if (SM_id == 15){
		arrayData[SM_id - 13] = c;	//goDir[2]
		SM_id++;
	}else if (SM_id > 15 && SM_id <= 17){
		arrayDataYII[SM_id - 16] = c;	//goY
		SM_id++;
	}else if (SM_id == 18){
		arrayData[SM_id - 15] = c;	//goDir[3]
		SM_id++;
	}else if (SM_id > 18 && SM_id <= 20){
		arrayAngGrip[SM_id - 19] = c;//Anggrip
		SM_id++;
		if(SM_id >= 21){
			getPackage = 1;
			SM_id = 1;
		}
	}
}

#INT_RDA               // receive data interrupt one time per one 
void UART1_Isr() {
    int c = getc();
    SM_RxD(c);
}

void control_inputX(int input, int direc){
	if(direc == 0){
		if(input >= 743 ){
			set_pwm_duty(1, 2000);
			output_bit(motorXI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorXII,0);
		}else if(input > 0 ){
			set_pwm_duty(1, (int)((input/743.0f)*2000));
			output_bit(motorXI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorXII,0);
		}else{
			set_pwm_duty(1, 0);
			output_bit(motorXI,0);
			output_bit(motorXII,0);
			}
	}	
	else if(direc == 1){
		if(input >= 743 ){
			set_pwm_duty(1, 2000);
			output_bit(motorXI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorXII,1);
		}else if(input > 0 ){
			set_pwm_duty(1, (int)((input/743.0f)*2000));
			output_bit(motorXI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorXII,1);
		}else{
			set_pwm_duty(1, 0);
			output_bit(motorXI,0);
			output_bit(motorXII,0);
		}
	}		
}


void control_inputY(int input, int direc){
	
if(direc == 0){
		if(input >= 743 ){
			set_pwm_duty(2, 2000);
			output_bit(motorYI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorYII,0);
		}else if(input > 0 ){
			set_pwm_duty(2, (int)((input/743.0f)*2000));
			output_bit(motorYI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorYII,0);
		}else{
			set_pwm_duty(2, 0);
			output_bit(motorYI,0);
			output_bit(motorYII,0);
			}
	}	
	else if(direc == 1){
		if(input >= 743 ){
			set_pwm_duty(2, 2000);
			output_bit(motorYI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorYII,1);
		}else if(input > 0 ){
			set_pwm_duty(2, (int)((input/743.0f)*2000));
			output_bit(motorYI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorYII,1);
		}else{
			set_pwm_duty(2, 0);
			output_bit(motorYI,0);
			output_bit(motorYII,0);
			
		}		
	}
}

void control_inputZ(int input, int direc){
	if(direc == 0){
		if(input >= 743 ){
			set_pwm_duty(3, 2000);
			output_bit(motorZI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorZII,0);
		}else if(input > 0 ){
			set_pwm_duty(3, (int)((input/743.0f)*2000));
			output_bit(motorZI,1); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorZII,0);
		}else{
			set_pwm_duty(3, 0);				
			output_bit(motorZI,0);
			output_bit(motorZII,0);
				}
	}	
	else if(direc == 1){
		if(input >= 743 ){
			set_pwm_duty(3, 2000);
			output_bit(motorZI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorZII,1);
		}else if(input > 0 ){
			set_pwm_duty(3, (int)((input/743.0f)*2000));
			output_bit(motorZI,0); //if 0, IN2->AXI@2 = clockwise 
			output_bit(motorZII,1);
		}else{
			set_pwm_duty(3, 0);
			output_bit(motorZI,0);
			output_bit(motorZII,0);
				
			}		
		}
	}

void move_posX(int pulse_x, int direc){
	int check = 1;
	while(check == 1){  
		int error = pulse_x - countX;
			error *= 6;
		//printf("error:%d\n",error);
		//delay_ms(10);

		if(abs(error) <= tolerance){
			control_inputX(0,direc);
			check = 0;	
		}else{
			control_inputX(error, direc); 

			
			
		}
	}
}

void move_posY(int pulse_y, int direc){
	int check = 1;
	while(check == 1){
		int error = pulse_y - countY;
			error *= 3.5;
		if(abs(error) <= tolerance){
			control_inputY(0, direc);
			check = 0;	
		}else{
			control_inputY(error, direc); 
		}
	}
}


void move_posZ(int pulse_z, int direc){
	int check = 1;
	while(check == 1){
	int error = pulse_z - countZ;
		error *= 2;
		if(abs(error) <= tolerance){
			control_inputZ(0, direc);	
			check = 0;
		}else{
			control_inputZ(error, direc);
		} 
	}
}


void set_Z(void){
	int check = 1;
	while(check == 1){ 
		if(input(lim_SW_Z) == 1){
			control_inputZ(0, 0);
			check = 0;
		}else if(input(lim_SW_Z) == 0){
			control_inputZ(700, 0);
		}
	}
}


void set_Zero(void){
	int loop = 1;
	int stateSWII = 0;
	while(loop == 1){
		if(stateSWII == 0){
			if(input(lim_SW_Y) == 1){
				control_inputY(0,1);
				stateSWII++;
			}else if(input(lim_SW_Y) == 0){
				control_inputY(700,0);
			}
		}else if(stateSWII == 1){  
			set_pwm_duty(4, 145);
			delay_ms(1000);
			set_pwm_duty(5, 100);
			delay_ms(1000);
			set_Z();
			stateSWII++;
		}else if(stateSWII == 2){  
			if(input(lim_SW_X) == 1){
				control_inputX(0,0);
				loop=0;
			}else if(input(lim_SW_X) == 0){
				control_inputX(700,0);
			}
		}
	} 
}

void moveXYZ(int x, int direcX, int y, int direcY, int z, int direcZ){

int loop = 1;
int stateSWIII = 0;
	while(loop == 1){
		if(stateSWIII == 0){
			move_posX(x, direcX);
			stateSWIII = 1;
		}else if(stateSWIII == 1){  
			move_posY(y, direcY);
			stateSWIII = 2;
		}else if(stateSWIII == 2){  
			move_posZ(z, direcZ);
			stateSWIII = 0;
			loop = 0;
		}
	} 
}	

void servo_Top(int degress){
	if(degress < 350){
		degress += 3;
		for(int i = 140;i <= degress;i++){
			set_pwm_duty(4, i);
			delay_ms(20);
		}
	}else{
		for(int i = 140;i <= degress;i++){
			set_pwm_duty(4, i);
			delay_ms(20);
		}	
	}
}

void servo_Under(int degress, int time){
	if(time == 0){
		for(int i = 90;i <= degress;i++){
			set_pwm_duty(5, i);
			delay_ms(20);
		}	
	}else if(time == 1){
		for(int i = 90;i <= degress;i++){
			set_pwm_duty(5, i);
			delay_ms(100);
		}
	}
}

#INT_EXT0
void INT_EXT_INPUT0 (void)
{	
		countX++;
}
#INT_EXT1
void INT_EXT_INPUT1 (void)
{	
		countY++;
}
#INT_EXT2
void INT_EXT_INPUT2 (void)
{	
		countZ++;
}
void Init_Interrupts()
{
	disable_interrupts(GLOBAL);
	
	clear_interrupt(INT_RDA);   // recommend style coding to confirm everything clear before use
    enable_interrupts(INT_RDA);

	enable_interrupts( INT_EXT0 );
	ext_int_edge( 0, L_TO_H ) ;

	enable_interrupts( INT_EXT1 );
	ext_int_edge( 1, L_TO_H ) ;

	enable_interrupts( INT_EXT2 );
	ext_int_edge( 2, L_TO_H ) ;
	
	setup_timer2(TMR_INTERNAL | TMR_DIV_BY_64 ,5000);
	setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8 ,TIME_PERIOD);


	enable_interrupts(GLOBAL);

}

void main(){
	Init_Interrupts();

	setup_compare(1, COMPARE_PWM | COMPARE_TIMER3);
	setup_compare(2, COMPARE_PWM | COMPARE_TIMER3);
	setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);

	setup_compare(4, COMPARE_PWM | COMPARE_TIMER2);
	setup_compare(5, COMPARE_PWM | COMPARE_TIMER2);
	set_Zero();
	int stateII = 0;
	int stateAll =0;
	while(TRUE){
			stateAll = 0;
			stateII = 0;
			countX = 0;
			countY = 0;
			countZ = 0;
			//set_pwm_duty(5, 90);//for 5,up is 250,down is 100 ServoTop
			/*if(stateII ==0){
 				set_pwm_duty(4, 560);//for 4,up is 580,down is 80, center is 330 ServoUnder
 				delay_ms(5000);
				set_pwm_duty(4, 350);
				delay_ms(5000);
				set_pwm_duty(4, 145);
				delay_ms(5000);
 				}stateII++;*/
			//} z => base is 7680+7680+1536+768 = 17664, groud is 20736, 13824,  3390 top on box
		int bagPosX, bagPosY, angle, goPosX, goPosY, angleGrip;
		if (getPackage >= 1){
			getPackage = 0;
			memcpy(&bagPosX, arrayDataXI, sizeof(bagPosX));
			memcpy(&bagPosY, arrayDataYI, sizeof(bagPosY));
			memcpy(&angle, arrayAng, sizeof(angle));
			memcpy(&goPosX, arrayDataXII, sizeof(goPosX));
			memcpy(&goPosY, arrayDataYII, sizeof(goPosY));
			memcpy(&angleGrip, arrayAngGrip, sizeof(angleGrip));
			move_posZ(7680, 1);

			while(stateAll==0){
				countX = 0;
				countY = 0;
				countZ = 0;
			
			if(stateII == 0){
				moveXYZ(bagPosX, arrayData[0], bagPosY, arrayData[1], 2300, 1);
				servo_Top(angle); //angle
				servo_Under(220, 0);//up tp gu.
				delay_ms(1000); 
				stateII++;
				
			}else if(stateII == 1){
				move_posZ(6400, 1);//To bag
				servo_Under(100, 0);
				delay_ms(1000);
				stateII++;
				
			}else if(stateII == 2){
				move_posZ(2800, 0); //3390
				servo_Top(angleGrip);
				delay_ms(1000);
				stateII++;
			
			}else if(stateII == 3){
				moveXYZ(goPosX, arrayData[2], goPosY, arrayData[3], 1000, 1);//6500, 5000, 3500, 1000
				delay_ms(500);
				stateII++;

			}else if(stateII == 4){
				servo_Under(200, 0);
				delay_ms(1000); 
				move_posZ(9000, 0);
				stateII++;

			}else{
				set_Zero();
				stateAll++;
				}
			}
		}	
	}
}


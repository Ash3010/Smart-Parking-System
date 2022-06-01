#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>
#include <Servo.h>
Servo motor;
LiquidCrystal lcd(2,3,4,5,6,7);


/*Using Hardware SPI of Arduino */
/*MOSI (11), MISO (12) and SCK (13) are fixed */
/*You can configure SS and RST Pins*/
#define SS_PIN 10  /* Slave Select Pin */
#define RST_PIN 9  /* Reset Pin */

/* Create an instance of MFRC522 */
MFRC522 mfrc522(SS_PIN, RST_PIN);
/* Create an instance of MIFARE_Key */
MFRC522::MIFARE_Key key;          

/* Set the block to which we want to write data */
/* Be aware of Sector Trailer Blocks */
int blockNum = 2;  
/* Create an array of 16 Bytes and fill it with data */
/* This is the actual data which is going to be written into the card */
byte blockData [16] = {"Electronics-Hub-"};

/* Create another array to read data from Block */
/* Legthn of buffer should be 2 Bytes more than the size of Block (16 Bytes) */
byte bufferLen = 18;
byte readBlockData[18];

MFRC522::StatusCode status;

void setup() 
{ lcd.begin(16,2);
motor.attach(8);
  /* Initialize serial communications with the PC */
  Serial.begin(9600);
  /* Initialize SPI bus */
  SPI.begin();
  /* Initialize MFRC522 Module */
  mfrc522.PCD_Init();
  //Serial.println("Scan a MIFARE 1K Tag to write data...");
}

void loop()
{
  /* Prepare the ksy for authentication */
  /* All keys are set to FFFFFFFFFFFFh at chip delivery from the factory */
  for (byte i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF;
  }
  /* Look for new cards */
  /* Reset the loop if no new card is present on RC522 Reader */
  if ( ! mfrc522.PICC_IsNewCardPresent())
  {lcd.setCursor(0,1);
  lcd.print("Punch Your Tag");
  motor.write(0);
    return ;
  }
  
  /* Select one of the cards */
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  { lcd.setCursor(0,1);
  lcd.print("Authorized");
    return;
  }
  //Serial.print("\n");
  //Serial.println("**Card Detected**");
  /* Print UID of the Card */
  //Serial.print(F("Card UID:"));
  for (byte i = 0; i < 4; i++)
  {
    //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    
  
    //Serial.print(mfrc522.uid.uidByte[i]);
    lcd.setCursor(0,1);
    lcd.print("Authorized");
    motor.write(90);
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    //Serial.print("\n");
  }
  delay(2000);
}

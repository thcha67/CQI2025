#include "../lib/espControl.h"
#include <Arduino.h>

/// @brief Créer une structure qui stock les instances de servos
/// @param servo1 
/// @param servo2 
/// @param servo3 
/// @return structure de servos
control_servoStruct_t control_setupServoStruct(Servo *servo1, Servo *servo2, Servo *servo3){
    control_servoStruct_t control_servos;
    control_servos.servo1 = servo1;
    control_servos.servo2 = servo2;
    control_servos.servo3 = servo3;
    return control_servos;
}

/// @brief Créer une structure qui stock les pins des moteurs et des servos
/// @param motor1Pin1 
/// @param motor1Pin2 
/// @param motor2Pin1 
/// @param motor2Pin2 
/// @param servo1 
/// @param servo2 
/// @param servo3 
/// @return structure qui contient les pins
const control_pins_t control_setupPins(const uint8_t motor1Pin1, const uint8_t motor1Pin2, const uint8_t motor2Pin1, const uint8_t motor2Pin2, const uint8_t servo1, const uint8_t servo2, const uint8_t servo3){
    control_pins_t pins;
    pins.motor1Pin1 = motor1Pin1;
    pins.motor1Pin2 = motor1Pin2;
    pins.motor2Pin1 = motor2Pin1;
    pins.motor2Pin2 = motor2Pin2;

    pins.servo1 = servo1;
    pins.servo2 = servo2;
    pins.servo3 = servo3;
    return pins;
}

/// @brief Fait avancer le robot
/// @param pins 
/// @param speed 
/// @param correction 
void forward(const control_pins_t * const pins, uint8_t speed, const float correction)
{
  speed = (uint8_t)map(speed, 0, 9, 0, 255);

  // TODO : Enelever ça 
  analogWrite(pins->motor1Pin1, speed);
  analogWrite(pins->motor1Pin2, 0);

  // Ajouter la correction par après
  analogWrite(pins->motor2Pin1, speed * correction);
  analogWrite(pins->motor2Pin2, 0);
}

/// @brief Fait reculer le robot
/// @param pins 
/// @param speed 
/// @param correction 
void backward(const control_pins_t * const pins, uint8_t speed, const float correction)
{
  speed = (uint8_t)map(speed, 0, 9, 0, 255);

  // TODO : Enelever ça 
  analogWrite(pins->motor1Pin1, 0);
  analogWrite(pins->motor1Pin2, speed);

  // Ajouter la correction par après
  analogWrite(pins->motor2Pin1, 0);
  analogWrite(pins->motor2Pin2, speed * correction);
}

/// @brief Setup les servos avec leurs pins correspondantes
/// @param servoStruct 
/// @param pins 
void control_setupServos(control_servoStruct_t *servoStruct, const control_pins_t * const pins)
{
  (servoStruct->servo1)->attach(pins->servo1, 620, 2420);
  (servoStruct->servo2)->attach(pins->servo2, 620, 2420);
  (servoStruct->servo3)->attach(pins->servo3, 620, 2420);

  (servoStruct->servo1)->write(0);
  (servoStruct->servo2)->write(0);
  (servoStruct->servo3)->write(0);

  (servoStruct->servo1)->detach();
  (servoStruct->servo2)->detach();
  (servoStruct->servo3)->detach();
}

/// @brief Modifier l'état des servos
/// @param servoStruct 
/// @param servo1_data 
/// @param servo2_data 
/// @param servo3_data 
void control_servos(control_t * control_data_ptr,const control_pins_t * pins, control_servoStruct_t * servoStruct)
{
  control_a_servo(servoStruct->servo1, control_data_ptr->attach_all_servos ,pins->servo1, &(control_data_ptr->servo1), &(control_data_ptr->prev_servo1));
  control_a_servo(servoStruct->servo2, control_data_ptr->attach_all_servos ,pins->servo2, &(control_data_ptr->servo2), &(control_data_ptr->prev_servo2));
  control_a_servo(servoStruct->servo3, control_data_ptr->attach_all_servos ,pins->servo3, &(control_data_ptr->servo3), &(control_data_ptr->prev_servo3));
}

/// @brief Modifier l'état d'un servo
/// Cette fonction permet de gérer l'attach et le detach du servo. Ainsi lorsqu'il est à idle le servo n'est pas attach
/// Ne modifie pas la valeur si elle est identique.
/// @param servo 
/// @param pin
/// @param new_data
/// @param prev_data
void control_a_servo(Servo * servo,const uint8_t pin ,const bool attach , uint16_t * new_data, uint16_t * prev_data)
{
    if(*new_data != *prev_data)
    {
      if(attach && (servo)->attached()) // Servo already attach. Just modify state.
      {
        (servo)->write(*new_data); 
      }
      else if(attach && !((servo)->attached())) // Servo is not attach and attach is required.
      {
        (servo)->attach(pin ,620, 2420); // 
        (servo)->write(*new_data);
      }
      else if (!attach && (servo)->attached()) // Servo is attached but not required.
      {
        (servo)->write(*new_data);
        (servo)->detach();
      }
      else if (!attach && !(servo)->attached()) // Servo is not attach and not required.
      {
        (servo)->attach(pin ,620, 2420);
        (servo)->write(*new_data);
        (servo)->detach();
      }
      *prev_data = *new_data;
    }
}


/// @brief Setup les GPIO de PWM pour les moteurs, et les met à 0
/// @param pins 
void control_setupMotors(const control_pins_t * const pins){
  pinMode(pins->motor1Pin1, OUTPUT);
  pinMode(pins->motor1Pin2, OUTPUT);
  pinMode(pins->motor2Pin1, OUTPUT);
  pinMode(pins->motor2Pin2, OUTPUT);

  analogWrite(pins->motor1Pin1, 0);
  analogWrite(pins->motor1Pin2, 0);
  analogWrite(pins->motor2Pin1, 0);
  analogWrite(pins->motor2Pin2, 0);
}

/// @brief Rendre le robot immobile
/// @param pins 
void control_setNullSpeed(const control_pins_t * const pins){
  analogWrite(pins->motor1Pin1, 0);
  analogWrite(pins->motor1Pin2, 0);
  analogWrite(pins->motor2Pin1, 0);
  analogWrite(pins->motor2Pin2, 0);
}

/// @brief Rotation du robot dans le sens anti-horaire
/// @param pins 
void rotate_counter_clock(const control_pins_t * const pins, uint8_t speed, const float correction){
  speed = (uint8_t)map(speed, 0, 9, 0, 255);

  analogWrite(pins->motor1Pin1, 0);
  analogWrite(pins->motor1Pin2, speed * correction);
  analogWrite(pins->motor2Pin1, speed * correction);
  analogWrite(pins->motor2Pin2, 0);
}

/// @brief Rotation du robot dans le sens horaire
/// @param pins 
void rotate_clock(const control_pins_t * const pins, uint8_t speed, const float correction){
  speed = (uint8_t)map(speed, 0, 9, 0, 255);

  analogWrite(pins->motor1Pin1, speed * correction);
  analogWrite(pins->motor1Pin2, 0);

  analogWrite(pins->motor2Pin1, 0);
  analogWrite(pins->motor2Pin2, speed * correction);
}

/// @brief  Met à jour les moteurs et les servos en fonction du contenu de la structure control
/// @param control 
/// @param pins 
void control_speed_orientation(const control_t * const control, const control_pins_t * const pins){
  if (control->direction == "None"){
    control_setNullSpeed(pins);
    return;
  }
  else if (control->direction == "w"){
    forward(pins, control->speed, control->correction);
  }
  else if (control->direction == "s"){
    backward(pins, control->speed, control->correction);
  }
  else if(control->direction == "d"){
    rotate_clock(pins, control->speed, control->correction);
  }
  else if(control->direction == "a"){
    rotate_counter_clock(pins, control->speed, control->correction);
  }
  else{
    Serial.println("ERROR: direction not found, setting speed to 0");
    control_setNullSpeed(pins);
  }
}

/// @brief Fonction générale qui met à jour les moteurs et les servos en fonction du contenu de la structure control
/// @param control_data_ptr 
/// @param pins 
/// @param servoStruct 
void control_update(control_t * control_data_ptr,const control_pins_t * const pins, control_servoStruct_t * const servoStruct){
  control_speed_orientation(control_data_ptr, pins);

  if(control_data_ptr->servo_is_modified)
  {
    control_servos(control_data_ptr, pins, servoStruct);
    control_data_ptr->servo_is_modified = false;
  }
}

/*
void control_servoSequence(control_servoStruct_t *servoStruct, control_t * control_data_ptr){
  unsigned long start = millis();
  control_servos(servoStruct, 90, 90, 90);
  while(millis() - start < 1000){
    // wait
  }
  control_servos(servoStruct, 0, 0, 0);
  while(millis() - start < 2000){
    // wait
  }
  control_servos(servoStruct, 180, 180, 180);
   while(millis() - start < 3000){
    // wait
  }
  // Reset the sequence flag to 0
  control_data_ptr->servo_in_sequence = false;
  Serial.println("Sequence done");

}
*/

/// @brief Imprime le contenu de la structure control sur le port série pour Debug
/// @param control 
void control_printDebug(control_t *control, unsigned long time){
  Serial.print("[");
  Serial.print(time);
  Serial.println("]");
  Serial.print("direction: ");
  Serial.println(control->direction);
  Serial.print("speed: ");
  Serial.println(control->speed);
  Serial.print("correction: ");
  Serial.println(control->correction);
  Serial.print("servo1: ");
  Serial.println(control->servo1);
  Serial.print("servo2: ");
  Serial.println(control->servo2);
  Serial.print("servo3: ");
  Serial.println(control->servo3);
}
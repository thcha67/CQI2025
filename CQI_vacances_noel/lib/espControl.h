#ifndef ESPCONTROL_H
#define ESPCONTROL_H

#include <stdint.h>
#include <Arduino.h>
#include <Servo.h>

typedef struct{
    Servo *servo1;
    Servo *servo2;
    Servo *servo3;

}control_servoStruct_t;

typedef struct{
  String direction = "None";
  uint16_t speed = 0;
  float correction = 0;
  uint16_t servo1 = 0;
  uint16_t servo2 = 0;
  uint16_t servo3 = 0;
  uint16_t prev_servo1 = 0;
  uint16_t prev_servo2 = 0;
  uint16_t prev_servo3 = 0;
  bool attach_all_servos = false;
  bool servo_is_modified = false;
}control_t;

typedef struct{
    //motor
    uint8_t motor1Pin1;
    uint8_t motor1Pin2;
    uint8_t motor2Pin1;
    uint8_t motor2Pin2;
    //servo
    uint8_t servo1;
    uint8_t servo2;
    uint8_t servo3;
    } control_pins_t;


control_servoStruct_t control_setupServoStruct(Servo *servo1, Servo *servo2, Servo *servo3);
const control_pins_t control_setupPins(const uint8_t motor1Pin1, const uint8_t motor1Pin2, const uint8_t motor2Pin1, const uint8_t motor2Pin2, const uint8_t servo1, const uint8_t servo2, const uint8_t servo3);
void forward(const control_pins_t * const pins, uint8_t speed, const float correction);
void backward(const control_pins_t * const pins, uint8_t speed, const float correction);
void control_setupServos(control_servoStruct_t *servoStruct, const control_pins_t * const pins);
void control_a_servo(Servo * servo,const uint8_t pin , const bool attach, uint16_t * new_data, uint16_t * prev_data);
void control_setupMotors(const control_pins_t * const pins);
void control_setNullSpeed(const control_pins_t * const pins);
void rotate_counter_clock(const control_pins_t * const pins, uint8_t speed, const float correction);
void rotate_clock(const control_pins_t * const pins, uint8_t speed, const float correction);
void control_speed_orientation(const control_t * const control, const control_pins_t * const pins);
void control_update(control_t * control_data_ptr, const control_pins_t * const pins, control_servoStruct_t * const servoStruct);
//void control_servoSequence(control_servoStruct_t *servoStruct, control_t * control_data_ptr);
void control_printDebug(control_t *control, unsigned long time);

#endif // ESPCONTROL_H
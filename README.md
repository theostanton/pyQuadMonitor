Quad_Monitor
============

Displays live Quadcopter data. 
Uses my FrameHandler. 

Demo video here https://www.youtube.com/watch?v=5kVJoPb2f80
Recorded with Quadcopter on table moved about with my hand. 

![Alt text](http://i.imgur.com/2XP6qCS.png?raw=true "Screenshots")


Communication to Quadcopter uses 3 byte packets in form :

      ID MSB LSB
      
      Where ID is one of :
      
      KPid 1  
      KIid 2  
      KDid 3  
      RATEid 4  
      COMPid 5  
      MAXINTEGRALid 6  
      PINGid 7  
      RXPINGid 8  
      THROTTLEid 29  
      YAWid 30  
      PITCHLid 31  
      ROLLid 32  
      
      and integer data is (MSB << 8) | LSB
  
Communication from Quadcopter receives string packets with data split by commas. First char is one of the following:
  
      A - Accelerometer  
      G - Gyroscope  
      M - Measured  
      D - Desired  
      E - Error  
      a - PID of motor A  
      b - PID of motor B  
      c - PID of motor C  
      d - PID of motor D  
  


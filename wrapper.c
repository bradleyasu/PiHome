/**
 * Backlight command line utility
 *
 * Simple command line utility for controlling the backlight of the PI LCD 
 * screen
 * 
 * Author: Bradley Sheets
 * Date: February 2018
 */
  #include <stdlib.h>
  #include <stdio.h>
  #include <string.h>
  #include <sys/types.h>
  #include <unistd.h>

  int main (int argc, char *argv[]) {
     setuid (0);

     if(argc < 1){
       printf("Please provide range between 15 and 255");
	     return 0;
     }

     char data[100];
     strcpy(data, "echo ");
     strcat(data, argv[1]);
     strcat(data, " > /sys/class/backlight/rpi_backlight/brightness");
     system(data);
     return 0;
   }

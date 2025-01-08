// bike rental system.
// available 5 bikes and 4 person wanted to access them.
// scope: no refilling of the fuel is done, limited fuel.
//      : each person get to go only one trip.
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>
#include<time.h>

pthread_mutex_t bike_mut[5];    //mutex lock for 5 bikes
int bike[5]={4,4,4,4,4};        //initial fuel levels on each bikes

void* routine(void* arg){
int counter=0;                  //counter to check how many times the person is iterated to get a bike
    for(int i=0;i<5;i++){       //loop to iterate around all 5 bikes
        if(pthread_mutex_trylock(&bike_mut[i])==0){ //try to lock, if succeeded, acquire bike and lock mutex
            int req_fuel=(rand()%60);       //simulate fuel requirement based on trip
            if(bike[i]>req_fuel){           //check if fuel req met
                counter=0;                  
                bike[i]-=req_fuel;                              //if met, take a trip 
                printf("fuel left %d on bike %d\n",bike[i],i);  //print fuel left on bike
                pthread_mutex_unlock(&bike_mut[i]);             //release the lock and break loop
                break;
            }
            else{                           //if not met, inc counter of number of bikes visited
                printf("fuel requirement not met...\n"); 
                counter++;
            }
            pthread_mutex_unlock(&bike_mut[i]); //release the lock of current bike
        }
        if(counter==4)          //if all bikes have been looked, break out of loop
            break;
        if(i==4)                //if end of loop reached, start from first
            i=0;
    }
}

int main(){
   srand(time(NULL)); 
   pthread_t p[10];
   for(int i=0;i<5;i++) 
        if(pthread_mutex_init(&bike_mut[i],NULL)!=0)
            perror("error initialising mutex");

   for(int i=0;i<4;i++)
        if(pthread_create(&p[i],NULL,&routine,NULL)!=0)
            perror("error creating thread...");

   for(int i=0;i<4;i++)
        if(pthread_join(p[i],NULL)!=0)
            perror("error joining thread...");

   for(int i=0;i<5;i++) 
        if(pthread_mutex_destroy(&bike_mut[i])!=0)
            perror("error destroying mutex... ");
   
   return 0;
}
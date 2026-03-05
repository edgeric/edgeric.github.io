#include<my_class_rt_e2.h>
class class1{
  run_slot(){
    +send_kpi() // zmq in publish mode (pub_socket3 - send TTI tick)
  }
}


class my_class_rt_e2{
    send_kpi(){
        while True:
            subscribe to pub_socket3 // get the TTI tick from RAN
            now subscribe to all other sockets serially
            package all the received metrics and send to EdgeRIC

    }
    get_control(){
        while True:
            subscribe to pub_socket3 // get the TTI tick from RAN
            recieve control signals from EdgeRIC - use conflate
            publish these control actions to respective sockets
    }
}
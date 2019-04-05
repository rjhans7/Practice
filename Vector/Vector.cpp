//
// Created by rudri on 3/29/2019.
//

#include "Vector.h"

    void UTEC::vector::push_back(const int &value) {
    if (_arr == nullptr){
        _arr = new int [_size]; //Creo el array
        _arr[_size] = value; //Asigno el valor a la primera posicion, size =0
        _size+=1; //Actualizo el valor del size
    }else{
        _arr[_size]=value;
        _size+=1; //Actualizo el valor del size
    }
    }

    void UTEC::vector::pop_back() {
        _arr[_size]=_arr[_size+1];
        _size-=1; //Actualizo el valor del size
    }

UTEC::vector::vector() : _arr{nullptr}, _size(0) {} //Creo un puntero del tipo int y lo inicializo en nullptr, a size le asigno el valor de 0
UTEC::vector::~vector() { delete []_arr;}

    int UTEC::vector::size() {return _size;}

    int UTEC::vector::get_item(int i) {return _arr[i];}

void UTEC::vector::insert(int pos, const int &value) {
    _arr[pos]=value;

}

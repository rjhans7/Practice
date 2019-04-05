//
// Created by rudri on 3/29/2019.
//

#include "Vector.h"

    void UTEC::vector::push_back(const int &value) {
    if (_arr == nullptr){
        _arr = new int [_size];
        _arr[_size] = value;
        _size+=1;
    }else{
        _arr[_size]=value;
        _size+=1;
    }
    }

    void UTEC::vector::pop_back() {
        _arr[_size]=_arr[_size+1];
        _size-=1; //Actualizo el valor del size
    }

UTEC::vector::vector() : _arr{nullptr}, _size(0) {}
UTEC::vector::~vector() { delete []_arr;}

    int UTEC::vector::size() {return _size;}

    int UTEC::vector::get_item(int i) {return _arr[i];}

void UTEC::vector::insert(int pos, const int &value) {
    _arr[pos]=value;

}

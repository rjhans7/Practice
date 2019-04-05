#include <iostream>
#include <vector>
#include <cassert>
#include "Vector.h"

using namespace std;

int main() {

    // Creando vectores
    vector<int> vec1;
    UTEC::vector vec2;

    // Agregando datos
    for (int i = 0; i < 100; ++i) {
        vec1.push_back(i);
        vec2.push_back(i);

        // Verificando cada dato
        assert(vec1[i] == vec2.get_item(i)); //asert verifica si son inguales, sino arroja un error que impide continuar
    }

    assert(vec1.size() == vec2.size());
    cout << "Paso push_back\n";

    // Borrando datos
    for (int i = 0; i < 20; ++i) {
        vec1.pop_back();
        vec2.pop_back();
    }
   assert(vec1.size() == vec2.size());

    // Verificando cada dato
    for (int j = 0; j < vec1.size(); ++j) {
        assert(vec1[j] == vec2.get_item(j));
    }
    cout << "Paso pop_back\n";

    // Agregando datos
    auto j = 0;
    for (int i = 40; i < 20; ++i) {
        vec1.insert(vec1.begin()+j, i);
        vec2.insert(j++, i);
    }

    assert(vec1.size() == vec2.size());

    // Verificando cada dato
    for (int i = 0; i < vec1.size(); ++i) {
        assert(vec1[i] == vec2.get_item(i));
    }

    cout << "Funciono Correctamente\n";
    return 0;
}
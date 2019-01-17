#include <iostream>

class Factorizator {
  private:
    int max_value;
    int factor[0];
  public:
    Factorizator(int max_value);
    int[] razl_na_mn(int ch);
};

Factorizator::Factorizator(int max_value) {
    this->max_value = max_value;

    int sieve[max_value + 1];
    this->factor = new int[max_value + 1];

    for (int i = 0; i<= max_value; i++){
        sieve[i] = i;
        factor[i] = i;
    }

    for (int i = 2; i <= max_value; i++ ){
        if (sieve[i] > 0) {
            for (int j = i + i; j <= max_value; j += i) {
                sieve[j] = 0;
                factor[j] = i;
            }
        }
    }
};


int[] Factorizator::razl_na_mn(int ch){
    int razl[] = new int[32];

    if (ch == 1) return new int[0];

    int d =  factor[ch];
    int cntr = 0;
    int iSimpleCounter = 0;
    while (ch != 1){
        if (d != factor[ch]){
            razl[iSimpleCounter++] = cntr;
            cntr = 0;
            d = factor[ch];
        }
        ch /= d;
        cntr++;
    }
    razl[iSimpleCounter++] = cntr;

    return Arrays.copyOf(razl, iSimpleCounter);
};

int main()
{
  std::cout << "Hello World!";
}
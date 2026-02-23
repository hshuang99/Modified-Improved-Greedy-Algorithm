#include <iostream>
#include <bitset>
#include <vector>
#include <cfloat>
#include <cmath>
#include <string>
#include <fstream>
#include <sstream>

#define epsilon 0.001
#define SIZE 32

int minm = 100;
int size_minm;

class Matrix{
public:
	std::bitset<SIZE> m[SIZE];

	Matrix(){};

	Matrix(std::bitset<SIZE> rhs[SIZE]){
		for(int i = 0; i < SIZE; i++){
            		m[i] = rhs[i];
		}
    	}

	Matrix(const Matrix& rhs){
		for(int i = 0; i < SIZE; i++){
			m[i] = rhs.m[i];
		}
	}

	Matrix(const std::vector<std::bitset<SIZE>>& str){
        	for(int i = 0; i < SIZE; i++){
            		m[i] = str[i];
        	}
    	}

	Matrix inverse(){
		std::bitset<SIZE> ret[SIZE];
		std::bitset<SIZE> original[SIZE];
		std::bitset<SIZE> tmp;
		for(int i = 0; i < SIZE; i++){
			ret[i][i] = 1;
			original[i] = m[i];
		}	
		for(int i = 0; i < SIZE; i++){
			if(original[i][i] == 0){
				int k;
				for(int j = i + 1; j < SIZE; j++){
					if(original[j][i] == 1){
						k = j;
						break;
					}
				}
				swap(original[i], original[k]);
				swap(ret[i], ret[k]);
			}
			for(int j = i + 1; j < SIZE; j++){
				if(original[j][i] == 1){
					original[j] ^= original[i];
					ret[j] ^= ret[i];
				}
			}
		}
		for(int i = SIZE - 1; i > 0; i--){
			for(int j = i - 1; j >= 0; j--){
				if(original[j][i] == 1){
					original[j] ^= original[i];
					ret[j] ^= ret[i];
				}
			}
		}
		Matrix res(ret);
		return res;
	}


	Matrix transpose(){
		std::bitset<SIZE> ret[SIZE];
		for(int i = 0; i < SIZE; i++){
			for(int j = 0; j < SIZE; j++){
				ret[i][j] = this->m[j][i];
			}            
		}
		Matrix res(ret);
		return res;
	}
    
	Matrix row_i2j(int i, int j){
		Matrix ret = *this;
		ret.m[j] ^= ret.m[i];
		return ret;
	}
    
	Matrix col_i2j(int i, int j){
		Matrix ret = *this;
		for(int k = 0; k < SIZE; k++){
			if(ret.m[k][i]){
				ret.m[k].flip(j);
			}
		}
		return ret;
	}

	double cost_func(int i){
		double ret;
		switch(i){
			case 1: ret = this->h_sq(); break;
			case 2: ret = this->H_sq(); break;
			case 3: ret = this->h_prod(); break;
			case 4: ret = this->H_prod(); break;
		}
		return ret;
	}

	double h_sq(){
		double ret = 0;
		for(int i = 0; i < SIZE; i++){
			ret += m[i].count() * m[i].count();
		}
		return ret;
	}

	double h_sq_t(){
		double ret = 0;
		for(int i = 0; i < SIZE; i++){
			int counter = 0;
			for(int j = 0; j < SIZE; j++){
				if(m[j][i] == 1){
					counter++;
				}
			}
			ret += counter * counter;
		}
		return ret;
	}

	double H_sq(){
		return this->h_sq() + this->inverse().h_sq_t();
	}

	double h_prod(){
		double ret = 0;
		for(int i = 0; i < SIZE; i++){
			ret += log2(m[i].count());
		}
		return ret;
	}

	double h_prod_t(){
		double ret = 0;
		for(int i = 0; i < SIZE; i++){
			int counter = 0;
			for(int j = 0; j < SIZE; j++){
				if(m[j][i] == 1){
					counter++;
				}
			}
			ret += log2(counter);
		}
		return ret;
	}

	double H_prod(){
		return this->h_prod() + this->inverse().h_prod();
	}

	bool Can_depth_one(){
		for(int i = 0; i < SIZE; i++){
			if(m[i].count() > 2){
				return false;
			}
		}

		int counter_col[SIZE]{};
		for(int i = 0; i < SIZE; i++){
			int counter = 0;
			for(int j = 0; j < SIZE; j++){
				if(m[j][i]){
					counter++;
				}
			}
			if(counter > 2){
				return false;
			}
			counter_col[i] = counter;
		}

		int counter_r[SIZE]{};
		int counter_c[SIZE]{};
		for(int i = 0; i < SIZE; i++){
			for(int j = 0; j < SIZE; j++){
				if(m[i][j] && m[i].count() == 2 && counter_col[j] == 2){
					counter_r[i]++, counter_c[j]++;
				}
				if(counter_r[i] > 1 || counter_c[j] > 1){
					return false;
				}
			}
		}
		return true;
	}

	void print(){
		for(int i = 0; i < SIZE; i++){
			for(int j = 0;j < SIZE; j++){
				std::cout << m[i][j] << ' ';
			}
			std::cout << std::endl;
		}
	}
};

typedef struct{
	int control;
	int target;
	int type;//0 for row and  1 for col.
}Oper;

void greedy_sq(Matrix matrix){
	/*
	In this algorithm, we decided choose the square cost function for minic the greedy0 algorithm from source
	*/
	Matrix origin = matrix;

	Matrix inverse = matrix.inverse();
	Matrix tmp_matrix;
	Matrix tmp_inverse;

	inverse.print();

	int depth = 0; //d <-- 0
	double minm_cost = DBL_MAX; //initial setting largest floating-number depends on CPU
	double tmp_cost;

	std::vector<Oper> select_list; //List
	std::vector<Oper> layer_r, layer_c;
	std::vector<std::vector<Oper>> layers_r, layers_c;
	std::bitset<SIZE> row_visi, col_visi;
	std::vector<Oper> row_op, col_op;

	bool one = false;//can_one <-- false
	
	//
	while(matrix.cost_func(1)+inverse.transpose().cost_func(1) > ((2*SIZE)+epsilon)){
		select_list.clear();
		minm_cost = std::fmax(matrix.cost_func(1)+inverse.transpose().cost_func(1), matrix.transpose().cost_func(1) + inverse.cost_func(1));
		//calculate for the H_{sqr}
		if(!one){
			for(int i =0; i< SIZE; i++){
				if(row_visi[i] == 1){
					continue;
				}
				for(int j = 0; j < SIZE; j++){
					if(row_visi[j] == 1 || j == i){
						continue;
					}
					tmp_matrix = matrix.row_i2j(i, j);
					tmp_inverse = inverse.col_i2j(j, i);
					tmp_cost = tmp_matrix.cost_func(1) + tmp_inverse.transpose().cost_func(1);
			
					if(tmp_cost < minm_cost + epsilon){
						if(tmp_cost < minm_cost - epsilon){
							select_list.clear();
							Oper oper = {i, j, 0};
							select_list.push_back(oper);
							minm_cost = tmp_cost;
						}else{
							Oper oper = {i, j, 0};
							select_list.push_back(oper);
						}
					}
				}
			}
		}
		//calculate for the H_{sqc}
		for(int i = 0; i < SIZE; i++){
			if(col_visi[i] == 1){
				continue;
			}
			for(int j = 0;j < SIZE; j++){
				if(col_visi[j] == 1 || j == i){
					continue;
				}
				tmp_matrix = matrix.col_i2j(i, j);
				tmp_inverse = inverse.row_i2j(j, i);
				tmp_cost = tmp_matrix.transpose().cost_func(1) + tmp_inverse.cost_func(1);
				if(tmp_cost < minm_cost + epsilon){
					if(tmp_cost < minm_cost - epsilon){
						select_list.clear();
						Oper oper = {i, j, 1};
						select_list.push_back(oper);
						minm_cost = tmp_cost;
					}else{
						Oper oper = {i, j, 1};
						select_list.push_back(oper);
					}
				}
			}
		}

		if(select_list.size() == 0){
			if(layer_r.size()){
				layers_r.push_back(layer_r);
				layer_r.clear();
				row_visi = 0;
			}
			if(layer_c.size()){
				layers_c.push_back(layer_c);
				layer_c.clear();
				col_visi = 0;
			}
			if(matrix.Can_depth_one()){
				one = true;
			}
		}else{
			int random = rand() % select_list.size();
			auto [c, t, t01] = select_list[random];
			if(t01 == 0){
				matrix = matrix.row_i2j(c, t);
				inverse = inverse.col_i2j(t, c);
				layer_r.push_back({c, t, 0});
				row_op.push_back({c, t, 0});
				if(row_visi == 0){
					depth++;
				}
				row_visi[c] = 1;
				row_visi[t] = 1;
			}else{
				matrix = matrix.col_i2j(c, t);
				inverse = inverse.row_i2j(t, c);
				layer_c.push_back({c, t, 1});
				col_op.push_back({c, t, 1});
				if(col_visi == 0){
					depth++;
				}
				col_visi[c] = 1;
				col_visi[t] = 1;
			}
		}

		if(depth > 100){
			std::cout << "depth too large" << std::endl;
			matrix.print();
			break;
		}
	}
	
	if(layer_r.size()){
		layers_r.push_back(layer_r);
		layer_r.clear();
		row_visi = 0;
	}

	if(layer_c.size()){
		layers_c.push_back(layer_c);
		layer_c.clear();
		col_visi = 0;
	}

	//Print the reduced result
	Matrix reducedMatrix = origin;
	int size = 0;
	for(auto [c, t, _]: row_op){
		reducedMatrix = reducedMatrix.row_i2j(c, t), size++;
	}
	for(auto [c, t, _]: col_op){
		reducedMatrix = reducedMatrix.col_i2j(c, t), size++;
	}

	bool ok = true;
	for(int i = 0; i < SIZE; i++){
		if(reducedMatrix.m[i] != matrix.m[i]){
			ok = false;
			std::cout << i << "-th row diff" << std::endl;
		}
	}
	
	if(depth > minm || (depth == minm && size >= size_minm) || !ok){
		return;
	}

	minm = depth;
	size_minm = size;
	std::cout << "32-block size for Square Cost that the depth is: " << minm << " and size is: " << size_minm << std::endl;

	//record the permutation matrix
	int permutationMatrix[SIZE];
	
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			if(matrix.m[i][j] == 1){
				permutationMatrix[i] = j;
			}
		}
	}

	std::vector<Oper> sequence;
	std::vector<std::vector<Oper>> layers;

	for(int i = 0;i < col_op.size(); i++){
		auto [t, c, _] = col_op[i];
		sequence.push_back({c, t, 1});
	}

	for(int i = row_op.size()-1; i >= 0; i--){
		auto [c, t, _] = row_op[i];
		sequence.push_back({permutationMatrix[c], permutationMatrix[t], 0});
	}

	for(auto& l: layers_c){
		std::vector<Oper> nl;
		for(auto [t, c, _]: l){
			nl.push_back({c, t, 1});
		}
		layers.push_back(nl);
	}
	
	reverse(layers_r.begin(), layers_r.end());
	
	for(auto& l: layers_r){
		std::vector<Oper> nl;
		for(auto [c, t, _]: l){
			nl.push_back({permutationMatrix[c], permutationMatrix[t], 0});
		}
		layers.push_back(nl);
	}

	std::string result = "result/";
	std::ofstream f_layer(result + "Square layers 32 square_cost_function_test", std::ios::app);
	for(auto& l: layers){
		for(auto [t, c, _]: l){
			f_layer << t << ' ' << c << ' ';
		}
		f_layer << std::endl;
	}
	f_layer << "CNOT: " << sequence.size() << " depth: " << layers.size() << std::endl << std::endl;

	std::ofstream fout(result + "Square seq 32 square_cost_function_testing_seq", std::ios::app);
	for(int i = 0; i < sequence.size(); i++){
		fout << sequence[i].control << ' ' << sequence[i].target << ' ' << sequence[i].type << std::endl;
	}
	fout << "CNOT: " << sequence.size() << std::endl << std::endl;

	Matrix verify;
	for(int i = 0; i < SIZE; i++){
		verify.m[i][i] = 1;
	}
    
	for(int i = 0; i < sequence.size(); i++){
		verify = verify.row_i2j(sequence[i].control, sequence[i].target);
	}
	for(int i = 0; i < SIZE; i++){
		bool ok = false;
		for(int j = 0; j < SIZE; j++){
			if(verify.m[i] == origin.m[j]){
				ok = true;
			}
		}
		if(!ok){
			std::cout << "row " << i << " does not exist." << std::endl;
		}
	}

	fout.close();
}


void greedy_prod(Matrix matrix){
	/*
	In this algorithm, we decided choose the product cost function for minic the greedy_origin algorithm from source
	*/
	Matrix origin = matrix;

	Matrix inverse = matrix.inverse();
	Matrix tmp_matrix;
	Matrix tmp_inverse;

	int depth = 0; //d <-- 0
	double minm_cost = DBL_MAX; //initial setting largest floating-number depends on CPU
	double tmp_cost;

	std::vector<Oper> select_list; //List
	std::vector<Oper> layer_r, layer_c;
	std::vector<std::vector<Oper>> layers_r, layers_c;
	std::bitset<SIZE> row_visi, col_visi;
	std::vector<Oper> row_op, col_op;

	bool one = false;//can_one <-- false
	
	//
	while(matrix.cost_func(3)+inverse.transpose().cost_func(3) > epsilon){
		select_list.clear();
		minm_cost = std::fmax(matrix.cost_func(3)+inverse.transpose().cost_func(3), matrix.transpose().cost_func(3)+inverse.cost_func(3));

		//calculate for the H_{prodr}
		if(!one){
			for(int i = 0; i< SIZE; i++){
				if(row_visi[i] == 1){
					continue;
				}
				for(int j = 0; j < SIZE; j++){
					if(row_visi[j] == 1 || j == i){
						continue;
					}
					tmp_matrix = matrix.row_i2j(i, j);
					tmp_inverse = inverse.col_i2j(j, i);
					tmp_cost = tmp_matrix.cost_func(3) + tmp_inverse.transpose().cost_func(3);
			
					if(tmp_cost < minm_cost + epsilon){
						if(tmp_cost < minm_cost - epsilon){
							select_list.clear();
							Oper oper = {i, j, 0};
							select_list.push_back(oper);
							minm_cost = tmp_cost;
						}else{
							Oper oper = {i, j, 0};
							select_list.push_back(oper);
						}
					}
				}
			}
		}
		//calculate for the H_{prodc}
		for(int i = 0; i < SIZE; i++){
			if(col_visi[i] == 1){
				continue;
			}
			for(int j = 0;j < SIZE; j++){
				if(col_visi[j] == 1 || j == i){
					continue;
				}
				tmp_matrix = matrix.col_i2j(i, j);
				tmp_inverse = inverse.row_i2j(j, i);
				tmp_cost = tmp_matrix.transpose().cost_func(3) + tmp_inverse.cost_func(3);
				if(tmp_cost < minm_cost + epsilon){
					if(tmp_cost < minm_cost - epsilon){
						select_list.clear();
						Oper oper = {i, j, 1};
						select_list.push_back(oper);
						minm_cost = tmp_cost;
					}else{
						Oper oper = {i, j, 1};
						select_list.push_back(oper);
					}
				}
			}
		}

		if(select_list.size() == 0){
			if(layer_r.size()){
				layers_r.push_back(layer_r);
				layer_r.clear();
				row_visi = 0;
			}
			if(layer_c.size()){
				layers_c.push_back(layer_c);
				layer_c.clear();
				col_visi = 0;
			}
			//if(matrix.Can_depth_one()){
			//	one = true;
			//}
		}else{
			int random = rand() % select_list.size();
			auto [c, t, t01] = select_list[random];
			if(t01 == 0){
				matrix = matrix.row_i2j(c, t);
				inverse = inverse.col_i2j(t, c);
				layer_r.push_back({c, t, 0});
				row_op.push_back({c, t, 0});
				if(row_visi == 0){
					depth++;
				}
				row_visi[c] = 1;
				row_visi[t] = 1;
			}else{
				matrix = matrix.col_i2j(c, t);
				inverse = inverse.row_i2j(t, c);
				layer_c.push_back({c, t, 1});
				col_op.push_back({c, t, 1});
				if(col_visi == 0){
					depth++;
				}
				col_visi[c] = 1;
				col_visi[t] = 1;
			}
		}

		if(depth > 100){
			std::cout << "depth too large" << std::endl;
			matrix.print();
			break;
		}
	}
	
	if(layer_r.size()){
		layers_r.push_back(layer_r);
		layer_r.clear();
		row_visi = 0;
	}

	if(layer_c.size()){
		layers_c.push_back(layer_c);
		layer_c.clear();
		col_visi = 0;
	}

	//Print the reduced result
	Matrix reducedMatrix = origin;
	int size = 0;
	for(auto [c, t, _]: row_op){
		reducedMatrix = reducedMatrix.row_i2j(c, t), size++;
	}
	for(auto [c, t, _]: col_op){
		reducedMatrix = reducedMatrix.col_i2j(c, t), size++;
	}

	bool ok = true;
	for(int i = 0; i < SIZE; i++){
		if(reducedMatrix.m[i] != matrix.m[i]){
			ok = false;
			std::cout << i << "-th row diff" << std::endl;
		}
	}
	
	if(depth > minm || (depth == minm && size >= size_minm) || !ok){
		return;
	}

	minm = depth;
	size_minm = size;
	std::cout << "32-block size for Product Cost that the depth is: " << minm << " and size is: " << size_minm << std::endl;

	//record the permutation matrix
	int permutationMatrix[SIZE];
	
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			if(matrix.m[i][j] == 1){
				permutationMatrix[i] = j;
			}
		}
	}

	std::vector<Oper> sequence;
	std::vector<std::vector<Oper>> layers;

	for(int i = 0;i < col_op.size(); i++){
		auto [t, c, _] = col_op[i];
		sequence.push_back({c, t, 1});
	}

	for(int i = row_op.size()-1; i >= 0; i--){
		auto [c, t, _] = row_op[i];
		sequence.push_back({permutationMatrix[c], permutationMatrix[t], 0});
	}

	for(auto& l: layers_c){
		std::vector<Oper> nl;
		for(auto [t, c, _]: l){
			nl.push_back({c, t, 1});
		}
		layers.push_back(nl);
	}
	
	reverse(layers_r.begin(), layers_r.end());
	
	for(auto& l: layers_r){
		std::vector<Oper> nl;
		for(auto [c, t, _]: l){
			nl.push_back({permutationMatrix[c], permutationMatrix[t], 0});
		}
		layers.push_back(nl);
	}

	std::string result = "result/";
	std::ofstream f_layer(result + "Product layers 32 square_cost_function_test", std::ios::app);
	for(auto& l: layers){
		for(auto [t, c, _]: l){
			f_layer << t << ' ' << c << ' ';
		}
		f_layer << std::endl;
	}
	f_layer << "CNOT: " << sequence.size() << " depth: " << layers.size() << std::endl << std::endl;

	std::ofstream fout(result + "Product seq 32 square_cost_function_testing_seq", std::ios::app);
	for(int i = 0; i < sequence.size(); i++){
		fout << sequence[i].control << ' ' << sequence[i].target << ' ' << sequence[i].type << std::endl;
	}
	fout << "CNOT: " << sequence.size() << std::endl << std::endl;

	Matrix verify;
	for(int i = 0; i < SIZE; i++){
		verify.m[i][i] = 1;
	}
    
	for(int i = 0; i < sequence.size(); i++){
		verify = verify.row_i2j(sequence[i].control, sequence[i].target);
	}
	for(int i = 0; i < SIZE; i++){
		bool ok = false;
		for(int j = 0; j < SIZE; j++){
			if(verify.m[i] == origin.m[j]){
				ok = true;
			}
		}
		if(!ok){
			std::cout << "row " << i << " does not exist." << std::endl;
		}
	}

	fout.close();
}

int main(){
	Matrix aes;

	std::ifstream aes_content ("./AES.txt");
	
	if(!aes_content){
		std::cerr << "Unable to open the file";
		return 1;
	}
	
	std::vector<std::vector<int>> AES_Mapping;
	std::string line;

	while(std::getline(aes_content, line)){
		std::vector<int> row;
		std::stringstream ss(line);
		int value;
	
		while(ss >> value){
			row.push_back(value);
		}
		AES_Mapping.push_back(row);
	}

	aes_content.close();

	int aes_i = 0;
	
	for(const auto& row : AES_Mapping){
		int aes_j = 0;
		for(int val : row){
			aes.m[aes_i][aes_j] = val;
			aes_j++;
		}
		aes_i++;
	}


	//execution the cost function	
	greedy_sq(aes);	
	//greedy_prod(aes);

	return 0;
}

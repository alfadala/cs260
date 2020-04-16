#include<iostream>//header file included to use cout,cin in following code
using namespace std;

/******************Subroutine to display marble count***************************/
void displayCount(unsigned long long C){
	printf("Currently there are %llu marbles in the bag",C);
}
//Main function where code starts and ends
int main(){
	unsigned long long m_Count=0;// Variable to store marble count in positive integers. long long datatype is used for ultra huge numbers.
	char choice;
	cout<<"How many marbles do you want to start with?: ";//Simple prompt to enter starting marbles in bag
	cin>>m_Count;//Taking starting marble count from user.
	do{//Do loop which must run 1 time atleast
		displayCount(m_Count);//Invoking marble count display function
		cout<<"\nEnter (+,-) to add marble or remove marble and any other character to exit: ";//Simple prompt for operations.
		cin>>choice;//Variable to hold the operational characters
		if(choice=='+'){//Testing for entered choice of operation
				m_Count+=1;//Increment marble count by 1
			}
		else if(choice=='-'){
				if(m_Count==0){
					cout<<"Empty Bag! There are no marbles to remove..\n";
				}
				else{
					m_Count-=1;	//Decrement marble count by 1
				}				
			}
		else{
			cout<<"\nExiting...";
		}
	}while(choice=='+' || choice=='-');//Exit loop or program if user enters any choice other than +,-
	return 0;//Code ends here
}
/*DESIGN:
1-Creating nec variables to store marble count and a character choice of operations
2-Taking starting marble count to initialize marble count variable.
3-Taking operation (increment,decrement,exit) from user
4-Decision statements to increment or decrement on the basis of entered choice
5-See if user wants to repeat or exit, if yes then loop back to step 3. If no, show exit prompt and end program.
\
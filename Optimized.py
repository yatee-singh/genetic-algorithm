from SetCoveringProblemCreator import *
import time
import pandas as pd
import openpyxl
import plotly.graph_objects as go
import numpy as np
def generate_bitmask(one_to_hundred,totalSets):
    bit = [False for _ in range(totalSets)]
    cnt=0
    for i in range(100):
        limit=len(one_to_hundred[i])
        r=random.randint(0, limit-1)
        # print(one_to_hundred[i][r])
       
        if(bit[one_to_hundred[i][r]]==False):
            cnt+=1
        bit[one_to_hundred[i][r]]=True

        # r=random.randint(0,1)
        # bit[i]=bool(r)
        # cnt+=r

    # print(cnt)
    return bit

def fitness(x,totalSets,total_subsets):
    cnt=0

    for i in x:
        if i==True:
            cnt+=1
    
    cover=0

    one_to_hundred=[0 for _ in range(100)]
    for i in range(len(x)):
        if (x[i]==True):
            for y in total_subsets[i]:
                if (one_to_hundred[y-1]!= True):
                    cover+=1
                    one_to_hundred[y-1]=True

    deviation=(100-cover)

    return (-cnt)+10*cover


def pick_two_elements_proportional_to_value(population,totalSets,total_subsets):
    # Pick two elements with probability proportional to their values
    elements=[]
    for x in population:
        elements.append(fitness(x,totalSets=totalSets,total_subsets=total_subsets))

    for i in range(len(elements)):
        elements[i]=1.1**elements[i]
        
    picked_elements = random.choices(population, weights=elements, k=2)
    return picked_elements



def reproduce(x,y):
    n=len(x)
    c=random.randint(0,n)
    child = y[:c] + x[c:]
    return child 

# def valid(ind,child):

def mutate(child):
    l=len(child)
    for i in range(l):
        if(child[i]==True):
            r=random.randint(1,100)
            if(r<20):
                child[i]=False
        
        
        
    
    
    

#     return child


def main():
    sizes=[50,150,250,350]
    total_generations=50
    pop_size=50
    fig = go.Figure()
    x_axis=[]
    for i in range(1,total_generations+1):
        x_axis.append(i)

    for size in sizes:
        iterations=10
        excel=[]
        while(iterations>0):
            iter_gen=[]
            scp = SetCoveringProblemCreator()
            start_time = time.time()

        #    ********* You can use the following two functions in your program
            totalSets=size
            subsets = scp.Create(usize=100,totalSets=totalSets) # Creates a SetCoveringProblem with 200 subsets
            print(len(subsets))
            scp.WriteSetsToJson(subsets, 100, totalSets)
            print()
            total_subsets = scp.ReadSetsFromJson(f"scp_{totalSets}.json")
            totalSets=len(total_subsets)
            # print(total_subsets)
            # print(len(total_subsets))
            
            
        #    **********
        #    Write your code for find the solution to the SCP given in scp_test.json file using Genetic algorithm.


        #    Mapping each number from 1-100 to all corresponding sets that contain that number
            one_to_hundred = [[] for _ in range(100)]

            for i in range(len(total_subsets)):
                for x in total_subsets[i]:
                    one_to_hundred[x-1].append(i)
            
            # for i in range(100):
            #     print(i,' ',one_to_hundred[i])
            #     print()
            

        #   Initial state: defining a population
            population=[]
            

            for i in range(pop_size):
                bit=generate_bitmask(one_to_hundred=one_to_hundred,totalSets=totalSets)
                population.append(bit)
                # print(bit)
                # print()
            

            generations=0
            
            gen_array=[]
            while(generations<=total_generations):
                new_population=[]
                maxi_generation=-1e9
                for i in range(len(population)):
                    pick_two=pick_two_elements_proportional_to_value(population,totalSets=totalSets,total_subsets=total_subsets)
                    x=pick_two[0]
                    y=pick_two[1]
                    # print(x)
                    # print(y)
                    # print()
                    child=reproduce(x,y)

                    p=random.randint(0,101)
                    if(p<=20):
                        mutate(child)
                        #
                    fitness_child=fitness(child,total_subsets=total_subsets,totalSets=totalSets)
                    maxi_generation=max(maxi_generation,fitness_child)
                    
                    new_population.append(child)
                
                generations+=1
                gen_array.append(maxi_generation)
                # print("generattion : ",generations)
                maxi=0
                for x in population:
                    maxi=max(maxi,fitness(x,totalSets=totalSets,total_subsets=total_subsets))
                
                
                # print("fitness : ",maxi)
                population=new_population
            

            maxi_fit=-1e9
            solu=[]
            
            
            for x in population:
                f=fitness(x,totalSets=totalSets,total_subsets=total_subsets)
                if(f>maxi_fit):
                    maxi_fit=f
                    solu=x
            
            cnt=0

            for i in solu:
                if i==True:
                    cnt+=1
            
            cover=0

            one_to_hundred1=[0 for _ in range(100)]
            for i in range(len(solu)):
                if (solu[i]==True):
                    for y in total_subsets[i]:
                        if (one_to_hundred1[y-1]!= True):
                            cover+=1
                            one_to_hundred1[y-1]=True

            # for x in range(len(one_to_hundred1)):
            #     print(x)
            

            # print("Roll no : 2021A8PS2534G")
            # print("Number of subsets :",totalSets)
            # print("Solution :")
            # for i in range(len(solu)):
            #     str=f"{i+1}"+':'+f"{int(solu[i])}"+', '
            #     print(str,end="")
            end_time = time.time()
            # print()

            # print("fitness value of the best state :",maxi_fit)
            # print("Minimum number of subsets that can cover the Universal sets :",cnt)
            # print("Coverage : ",cover)
        # Calculate the elapsed time
            elapsed_time = end_time - start_time
            print(f"Time taken: {elapsed_time} seconds")
            iter_gen.append(gen_array)
            iterations-=1
        

        # Convert the list of arrays to a numpy array
        arrays_np = np.array(iter_gen)

        # Calculate the element-wise average
        average_array = np.mean(arrays_np, axis=0)
        std_dev_columns = np.std(arrays_np, axis=0)
        fig.add_trace(go.Scatter(x=x_axis, y=average_array,
                mode='lines',
                name=size))
        print(size)
        print("avergae of all generations")
        
        print(average_array)
        print("std devation of all generasion")
        print(std_dev_columns)
        # writer = pd.ExcelWriter('pandas_to_excel_no_index_header.xlsx',engine='openpyxl', mode='a')
        # df = pd.DataFrame(excel)
        # df.to_excel(writer,sheet_name='S350_task1')
        # writer.save()
    fig.update_layout(
    title="Fitness Value Vs Generations High Probabity of mutation and Not Random Initial population",
    xaxis_title="Generations",
    yaxis_title="Fitness Value",
    
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
    fig.show()
    
    # df.to_excel('pandas_to_excel_no_index_header.xlsx', index=False, header=False)






   


if __name__=='__main__':
    main()
from SetCoveringProblemCreator import *
import time

def generate_bitmask(one_to_hundred,totalSets):
    bit = [False for _ in range(totalSets)]
    cnt=0
    for i in range(100):
        limit=len(one_to_hundred[i])
        r=random.randint(0, limit-1)   
        if(bit[one_to_hundred[i][r]]==False):
            cnt+=1
        bit[one_to_hundred[i][r]]=True

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

    return (-cnt)+10*cover


def pick_two_elements_proportional_to_value(population_fit,population):
    # Pick two elements with probability proportional to their values
    elements=[]

    for i in range(len(population_fit)):
        elements.append(1.1**population_fit[i][0])
        
    picked_elements = random.choices(population, weights=elements, k=2)
    return picked_elements



def reproduce(x,y):
    n=len(x)
    c=random.randint(0,n)
    child = y[:c] + x[c:]
    return child 

def mutate(child):
    l=len(child)
    while(True):
        r=random.randint(0,l-1)
        if(child[r]==True):
            # print(r)
            # print(child)
            child[r]=False
            
           
            break

def main():
    
    total_generations=100
    pop_size=100
    totalSets=350
    scp = SetCoveringProblemCreator()
    start_time = time.time()
    # subsets = scp.Create(usize=100,totalSets=totalSets) # Creates a SetCoveringProblem with 200 subsets
    # print(len(subsets))
    # scp.WriteSetsToJson(subsets, 100, totalSets)
    # print()
    total_subsets = scp.ReadSetsFromJson(f"scp_test.json")
    totalSets=len(total_subsets)
    

#    Mapping each number from 1-100 to all corresponding sets that contain that number
    one_to_hundred = [[] for _ in range(100)]

    for i in range(len(total_subsets)):
        for x in total_subsets[i]:
            one_to_hundred[x-1].append(i)
    
          
#   Initial state: defining a population
    population=[]
    

    for i in range(pop_size):
        bit=generate_bitmask(one_to_hundred=one_to_hundred,totalSets=totalSets)
        population.append(bit)
               
    generations=0
    
   

    while(time.time()-start_time<45 and generations<total_generations ):
        new_population=[]
        maxi_generation=-1e9
        population_fit=[]

        maxi=-1e9
        for i in range(len(population)):
            fit=fitness(population[i],total_subsets=total_subsets,totalSets=totalSets)
            population_fit.append([fit,population[i]])
            maxi=max(maxi,fit)


        for k in range(pop_size):
            if(population_fit[k][0]<0.6*maxi):
                population.remove(population_fit[k][1])
                population_fit.remove(population_fit[k])
            
        
        

        for i in range(pop_size):
            pick_two=pick_two_elements_proportional_to_value(population_fit=population_fit,population=population)
            x=pick_two[0]
            y=pick_two[1]
            child=reproduce(x,y)

            p=random.randint(0,101)
            if(p<=50):
                mutate(child)
                #
            fitness_child=fitness(child,total_subsets=total_subsets,totalSets=totalSets)
            maxi_generation=max(maxi_generation,fitness_child)
            
            new_population.append(child)
        
        generations+=1
        # print("Generation",generations)
        # print("maxi",maxi_generation)
       
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
            

    print("Roll no : 2021A8PS2534G")
    print("Number of subsets in scp_test.json file :",totalSets)
    print("Solution :")
    for i in range(len(solu)):
        str=f"{i+1}"+':'+f"{int(solu[i])}"+', '
        print(str,end="")
    
    print()

    print("Fitness value of the best state :",maxi_fit)
    print("Minimum number of subsets that can cover the Universal sets :",cnt)
  
    
# Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")


if __name__=='__main__':
    main()
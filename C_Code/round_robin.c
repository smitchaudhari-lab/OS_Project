#include <stdio.h>

int main() {

    int n,i,time=0,remain;
    int at[10], bt[10], rt[10];
    int wt[10], tat[10];
    int quantum;

    printf("Enter number of processes: ");
    scanf("%d",&n);

    remain = n;

    for(i=0;i<n;i++)
    {
        printf("Arrival time for P%d: ",i+1);
        scanf("%d",&at[i]);

        printf("Burst time for P%d: ",i+1);
        scanf("%d",&bt[i]);

        rt[i] = bt[i];
    }

    printf("Enter time quantum: ");
    scanf("%d",&quantum);

    while(remain!=0)
    {
        for(i=0;i<n;i++)
        {
            if(rt[i] > 0)
            {
                if(rt[i] <= quantum)
                {
                    time += rt[i];
                    rt[i] = 0;
                    remain--;

                    tat[i] = time - at[i];
                    wt[i] = tat[i] - bt[i];
                }
                else
                {
                    rt[i] -= quantum;
                    time += quantum;
                }
            }
        }
    }

    printf("\nProcess\tAT\tBT\tWT\tTAT\n");

    for(i=0;i<n;i++)
    {
        printf("P%d\t%d\t%d\t%d\t%d\n",i+1,at[i],bt[i],wt[i],tat[i]);
    }

    return 0;
}

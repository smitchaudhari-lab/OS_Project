#include <stdio.h>

int main() {

    int n,i;
    int at[10], bt[10], wt[10], tat[10];

    printf("Enter number of processes: ");
    scanf("%d",&n);

    for(i=0;i<n;i++)
    {
        printf("Arrival time for P%d: ",i+1);
        scanf("%d",&at[i]);

        printf("Burst time for P%d: ",i+1);
        scanf("%d",&bt[i]);
    }

    wt[0] = 0;

    for(i=1;i<n;i++)
    {
        wt[i] = wt[i-1] + bt[i-1];
    }

    for(i=0;i<n;i++)
    {
        tat[i] = wt[i] + bt[i];
    }

    printf("\nProcess\tAT\tBT\tWT\tTAT\n");

    for(i=0;i<n;i++)
    {
        printf("P%d\t%d\t%d\t%d\t%d\n",i+1,at[i],bt[i],wt[i],tat[i]);
    }

    return 0;
}


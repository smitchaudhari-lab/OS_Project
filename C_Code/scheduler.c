#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

// ===== VALIDATION =====
int isValidNumber(char *str) {
    if (str[0] == '\n') return 0;

    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == '\n') break;
        if (!isdigit(str[i])) return 0;
    }
    return 1;
}

// ===== SAFE INPUT =====
int getValidInput(char *msg) {
    char input[100];
    int value;

    while (1) {
        printf("%s", msg);

        if (fgets(input, sizeof(input), stdin) == NULL)
            continue;

        if (!isValidNumber(input)) {
            printf("❌ Invalid input! Enter positive numbers only.\n");
            continue;
        }

        value = atoi(input);

        if (value <= 0) {
            printf("❌ Value must be greater than 0.\n");
            continue;
        }

        return value;
    }
}

// ===== FCFS =====
void fcfs(int n, int *bt, int *at) {
    int *wt = (int*)malloc(n * sizeof(int));
    int *tat = (int*)malloc(n * sizeof(int));

    int time = 0;
    float avg_wt = 0, avg_tat = 0;

    for (int i = 0; i < n; i++) {
        if (time < at[i])
            time = at[i];

        wt[i] = time - at[i];
        time += bt[i];
        tat[i] = wt[i] + bt[i];

        avg_wt += wt[i];
        avg_tat += tat[i];
    }

    printf("\n--- FCFS ---\n");
    printf("PID\tAT\tBT\tWT\tTAT\n");

    for (int i = 0; i < n; i++)
        printf("%d\t%d\t%d\t%d\t%d\n", i+1, at[i], bt[i], wt[i], tat[i]);

    printf("\nAvg WT = %.2f\nAvg TAT = %.2f\n", avg_wt/n, avg_tat/n);

printf("\nGantt Chart:\n|");

int current_time = 0;

for (int i = 0; i < n; i++) {
    printf(" P%d |", i + 1);
}

printf("\n0");

current_time = 0;

for (int i = 0; i < n; i++) {
    current_time += bt[i];
    printf("   %d", current_time);
}

printf("\n");

    free(wt);
    free(tat);
}

// ===== SJF =====
void sjf(int n, int *bt, int *at) {
    int *wt = (int*)malloc(n * sizeof(int));
    int *tat = (int*)malloc(n * sizeof(int));
    int *visited = (int*)calloc(n, sizeof(int));

    int done = 0, time = 0;
    float avg_wt = 0, avg_tat = 0;

    while (done < n) {
        int idx = -1, min = 9999;

        for (int i = 0; i < n; i++) {
            if (at[i] <= time && !visited[i] && bt[i] < min) {
                min = bt[i];
                idx = i;
            }
        }

        if (idx != -1) {
            visited[idx] = 1;
            wt[idx] = time - at[idx];
            time += bt[idx];
            tat[idx] = wt[idx] + bt[idx];

            avg_wt += wt[idx];
            avg_tat += tat[idx];
            done++;
        } else {
            time++;
        }
    }

    printf("\n--- SJF ---\n");
    printf("PID\tAT\tBT\tWT\tTAT\n");

    for (int i = 0; i < n; i++)
        printf("%d\t%d\t%d\t%d\t%d\n", i+1, at[i], bt[i], wt[i], tat[i]);

    printf("\nAvg WT = %.2f\nAvg TAT = %.2f\n", avg_wt/n, avg_tat/n);

printf("\nGantt Chart:\n|");

for (int i = 0; i < n; i++) {
    printf(" P%d |", i + 1);
}

printf("\n0");

int current_time = 0;

for (int i = 0; i < n; i++) {
    current_time += bt[i];
    printf("   %d", current_time);
}

printf("\n");

    free(wt);
    free(tat);
    free(visited);
}

// ===== ROUND ROBIN =====
void roundRobin(int n, int *bt, int tq) {
    int *rem = (int*)malloc(n * sizeof(int));
    int *wt = (int*)calloc(n, sizeof(int));
    int *tat = (int*)malloc(n * sizeof(int));

    int time = 0, done;
    float avg_wt = 0, avg_tat = 0;

    for (int i = 0; i < n; i++)
        rem[i] = bt[i];

    do {
        done = 1;

        for (int i = 0; i < n; i++) {
            if (rem[i] > 0) {
                done = 0;

                if (rem[i] > tq) {
                    time += tq;
                    rem[i] -= tq;
                } else {
                    time += rem[i];
                    wt[i] = time - bt[i];
                    rem[i] = 0;
                }
            }
        }
    } while (!done);

    for (int i = 0; i < n; i++) {
        tat[i] = wt[i] + bt[i];
        avg_wt += wt[i];
        avg_tat += tat[i];
    }

    printf("\n--- ROUND ROBIN ---\n");
    printf("PID\tBT\tWT\tTAT\n");

    for (int i = 0; i < n; i++)
        printf("%d\t%d\t%d\t%d\n", i+1, bt[i], wt[i], tat[i]);

    printf("\nAvg WT = %.2f\nAvg TAT = %.2f\n", avg_wt/n, avg_tat/n);


printf("\nGantt Chart:\n|");

for (int i = 0; i < n; i++) {
    printf(" P%d |", i + 1);
}

printf("\n0");

int current_time = 0;

for (int i = 0; i < n; i++) {
    current_time += bt[i];
    printf("   %d", current_time);
}

printf("\n");

    free(rem);
    free(wt);
    free(tat);
}

// ===== MAIN =====
int main() {
    int n, *bt, *at, choice, tq;

    while (1) {
        printf("\n===== CPU Scheduling Simulator =====\n");
        printf("1. FCFS\n2. SJF\n3. Round Robin\n4. Exit\n");

        choice = getValidInput("Enter your choice: ");

        if (choice == 4) break;

        if (choice < 1 || choice > 4) {
            printf("❌ Invalid choice!\n");
            continue;
        }

        n = getValidInput("Enter number of processes: ");

        if (n > 10000) {
            printf("❌ Too many processes (limit 10000 for safety)\n");
            continue;
        }

        bt = (int*)malloc(n * sizeof(int));
        at = (int*)malloc(n * sizeof(int));

        if (bt == NULL || at == NULL) {
            printf("❌ Memory allocation failed!\n");
            return 1;
        }

        for (int i = 0; i < n; i++) {
            printf("\nProcess %d\n", i+1);
            at[i] = getValidInput("Arrival Time: ");
            bt[i] = getValidInput("Burst Time: ");
        }

        switch (choice) {
            case 1:
                fcfs(n, bt, at);
                break;

            case 2:
                sjf(n, bt, at);
                break;

            case 3:
                tq = getValidInput("Enter Time Quantum: ");
                roundRobin(n, bt, tq);
                break;
        }

        free(bt);
        free(at);
    }

    printf("Exiting...\n");
    return 0;
}

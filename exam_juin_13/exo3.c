#include <time.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stdbool.h>
#include <inttypes.h>

// on travaille sur des tableaux d'au plus TAILLE_MAX entiers
static const uint64_t TAILLE_MAX = 10;

// le type des cellule manipulees
struct cell_t {
    int64_t val; // valeur de la cellule
    struct cell_t *suiv; // pointeur vers la cellule suivante
};

// fonctions implantees dans le fichier assembleur
void echanger(int64_t[], uint64_t, uint64_t);
void placer_pivot(int64_t[], uint64_t, uint64_t*, uint64_t*);
void tab_vers_liste(int64_t[], uint64_t, struct cell_t **);

// une fonction d'affichage d'un tableau d'entiers signes
void afficher_tab(int64_t tab[], uint64_t taille)
{
    printf("  Contenu du tableau (taille = %" PRIu64 ") : ", taille);
    for (uint64_t i = 0; i < taille; i++) {
        printf("%" PRId64 " ", tab[i]);
    }
    puts("");
}

// une fonction d'affichage d'une liste d'entiers signes
void afficher_liste(struct cell_t *liste)
{
    printf("  Contenu de la liste : ");
    while (liste != NULL) {
        printf("%" PRId64 " -> ", liste->val);
        liste = liste->suiv;
    }
    puts("FIN");
}

// une fonction qui desalloue toutes les cellules de la liste 
void detruire_liste(struct cell_t *liste)
{
    while (liste != NULL) {
        struct cell_t *suiv = liste->suiv;
        free(liste);
        liste = suiv;
    }
}

int main(void)
{
    // un tableau d'entiers signes sur 64 bits
    int64_t tab[TAILLE_MAX];
    // initialisation du generateur de nombres aleatoires
    srand(time(NULL));
    // on remplit le tableau d'entiers aleatoires avec des valeurs
    //   dans [-9 .. 9]
    for (uint64_t i = 0; i < TAILLE_MAX; i++) {
        tab[i] = (rand() % 19) - 9;
    }
    // test de la fonction echanger
    puts("Echange d'elements :");
    afficher_tab(tab, TAILLE_MAX);
    for (uint64_t i = 0, j = TAILLE_MAX - 1; i < j; i++, j--) {
        echanger(tab, i, j);
        afficher_tab(tab, TAILLE_MAX);
    }
    puts("");
    // test de la fonction placer_pivot
    puts("Tableau initial :");
    afficher_tab(tab, TAILLE_MAX);
    puts("Placement du pivot :");
    uint64_t prem, der;
    int64_t piv = tab[TAILLE_MAX - 1];
    placer_pivot(tab, TAILLE_MAX - 1, &prem, &der);
    afficher_tab(tab, TAILLE_MAX);
    printf("  Pivot : %" PRId64 "\n", piv);
    printf("  Zone des inferieurs : ");
    if (prem == 0) {
        printf("vide\n");
    } else {
        printf("indices de 0 a %" PRIu64 "\n", prem - 1);
    }
    printf("  Zone des equivalents : indices de %" PRIu64 " a %" PRIu64 "\n",
            prem, der);
    printf("  Zone des superieurs : ");
    if (der == TAILLE_MAX - 1) {
        printf("vide\n");
    } else {
        printf("indices de %" PRIu64 " a %" PRIu64 "\n", der + 1,
                TAILLE_MAX - 1);
    }
    puts("");
    // test de la fonction tab_vers_liste
    struct cell_t *liste = NULL;
    puts("Liste equivalente au tableau :");
    tab_vers_liste(tab, TAILLE_MAX, &liste);
    afficher_liste(liste);
    detruire_liste(liste);
    return 0;
}


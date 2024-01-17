# TP2 stéganographie, signature, etc

>Antoine DEPOISIER & Jules FINCK

>Lien Github : https://github.com/Tann-dev/INFO002-TP2

### Question 1

Voici la commande utilisée pour encoder un message dans une image :

```shell
python main.py hide <input image> <message> <output image>
```

Avec un exemple d'utilisation

```shell
python main.py hide img\chablais-orig.png coucou img\chablais-coucou.png
```

Voici ensuitel a commande permettant de déchiffrer le message contenu dans l'image

```shell
python main.py unhide <input image> <size>
```

Test avec l'image précédemment crée

```shell
python main.py unhide img\chablais-coucou.png 6
```

### Question 2

Pour générer nos couple de clé publique/clé privé, il faut utiliser la commande :

```shell
python main.py generate_key
```

Les clés seront toutes deux stockées dans les fichier `private_key.pem` et `public_key.pem`.

Pour créer le signature d'un message, il faut utiliser la commande :

```shell
python main.py sign <message>
```

La signature sera contenu dans le fichier `signature.bin`

Pour créer le signature d'un message, il faut utiliser la commande :

```shell
python main.py verify <msg>
```

En lançant cette commande, le programme va vérifier si le contenu de la signature dans `signature.bin` est le même que le message  donnée en paramètre.

### Question 3

On peut générer un diplôme sans données cachées pour le moment, avec la commande :

```shell
python main.py make_degree <input image> <output image> <student_name> <mean_student>
```

Par exemple, avec cette commande, le dipolôme s'appelant `diplome-test.png` est généré.

```shell
python main.py make_degree img/diplome-BG.png test.png "Jules Finck" 18.5
```

### Question 4

Dans le diplome nous cachons une signature pour le nom de l'étudiant, sa note et la date d'émission du diplôme.

Cette signature sert à être sûr que les données du diplôme n'ont pas été trafiqué.

```shell
python main.py make_degree <input image> <output image> <student_name> <mean_student>
```

### Question 5

Voici la commande permettant de vérifier le diplôme :

```shell
python main.py verify_degree <input image> <message> <hash_size>
```

Si on prend l'exemple de : 

```shell
python main.py make_degree img/diplome-BG.png test.png "Jules Finck" 18.5
```

et que l'on vérifie le diplôme avec la commande : 

```shell
python main.py verify_degree test.png "2024-01-17Jules Finck18.5" 512
```

Le programme va nous dire si les données du diplôme sont valides.

Le message que l'on donne en entrée est de la former `<date><student_name><mean_student>`, avec une date au format `YYYY-MM-DD`.
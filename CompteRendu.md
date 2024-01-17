# Compte Rendu TP2 stéganographie, signature, etc

#### Antoine DEPOISIER & Jules FINCK

## Choix fonctionnels

les choix fonctionnels faits (choix de l'information cachée, présentation des informations "techniques", ...) et leur justification

## Choix technologiques

Nous avons choisis d'utiliser le langage python pour réaliser ce TP

les choix technologiques faits (langage, algorithme de signature, bibliothèques) et recommandations pour le produit final

## Description de notre solution

Nous aurions pour idée d'ajouter un QR-code dans le diplôme, qui redirigait vers un site qui permet en donnant l'image du diplôme de vérifier le message caché à l'intérieur du diplôme.Ce message caché étant la signature, le site analyserait si les données contenu dans le diplôme (date d'émission, note et nom de l'étudiant) sont conformes.

Mais si nous n'avons pas les documents d'identité de la personne, ou bien si la personne a le même nom qu'une autre, il serait facile d'usurper son identité. Pour ce faire, une autre solution serait de chacher l'image de l'étudiant dans le diplôme et d'avoir une IA qui compare la tête d'une personne, avec celle caché dans le diplôme. Ou bien, une empreinte digital ou rétinienne au lieu de la photo. Dans ce cas, pour que ces données ne soient pas modifiés, l'université possèderait dans une base de données les photos et empreintes digitales des étudiants.

## Documentation

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

## Conclusion

conclusion sur la faisabilité et l'intérêt du service
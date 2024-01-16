# TP2 stéganographie, signature, etc

>Antoine DEPOISIER & Jules FINCK

## Question 1

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

## Question 2

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


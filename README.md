# Software-Architecutre-And-Design

Laboratories for Discipline "Software architecture and design" in KAI 4 semestr 2 course

## Project needs

- To run the project you will need to have [python](https://www.python.org/downloads/) 3.10+

### Notes

- To generate diagram:

```
pyreverse -o dot -p <lab_number> -A -S .
unflatten -l 3 -c 5 classes_<lab_number>.dot | dot -Tpng -o my_diagram.png
```

import re

class AnalizadorLexico:
    def __init__(self, archivo_diccionario):
        """
        Inicializa el analizador léxico cargando el diccionario de palabras clave.
        
        Args:
            archivo_diccionario: Ruta al archivo del diccionario
        """
        self.palabras_clave = {}
        self.patron_identificador = re.compile(r'^[a-z][a-z0-9]*$')
        self.cargar_diccionario(archivo_diccionario)
    
    def cargar_diccionario(self, archivo):
        """
        Lee el archivo diccionario.txt y carga las palabras clave en un Hash Map.
        Formato esperado: lexema tipo_token
        
        Args:
            archivo: Ruta al archivo del diccionario
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        partes = linea.split()
                        if len(partes) == 2:
                            lexema, tipo_token = partes
                            self.palabras_clave[lexema] = tipo_token
            print(f"Diccionario cargado: {len(self.palabras_clave)} palabras clave")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo}")
            raise
        except Exception as e:
            print(f"Error al cargar el diccionario: {e}")
            raise
    
    def es_identificador(self, palabra):
        """
        Verifica si una palabra cumple con el patrón de identificador.
        Patrón: Una letra minúscula seguida de cero o más letras minúsculas o dígitos.
        Expresión Regular: [a-z][a-z0-9]*
        
        Args:
            palabra: Cadena a validar
            
        Returns:
            True si es un identificador válido, False en caso contrario
        """
        return bool(self.patron_identificador.match(palabra))
    
    def clasificar_token(self, palabra):
        """
        Clasifica una palabra según las reglas del analizador léxico:
        1. Verifica si es palabra clave (búsqueda en Hash Map - O(1))
        2. Verifica si es identificador válido (regex)
        3. Si no cumple ninguna regla, es un error léxico
        
        Args:
            palabra: Cadena a clasificar
            
        Returns:
            Tupla (tipo_token, lexema)
        """
        # Paso A: Verificar si es palabra clave
        if palabra in self.palabras_clave:
            return (self.palabras_clave[palabra], palabra)
        
        # Paso B: Verificar si es identificador válido
        if self.es_identificador(palabra):
            return ("IDENTIFICADOR", palabra)
        
        # Paso C: Error léxico
        return ("ERROR_LEXICO", palabra)
    
    def analizar_archivo(self, archivo_entrada, archivo_salida):
        """
        Analiza el archivo de entrada y genera el archivo de salida con los tokens.
        
        Args:
            archivo_entrada: Ruta al archivo de texto a analizar
            archivo_salida: Ruta al archivo de salida con los tokens
        """
        tokens = []
        
        try:
            # Leer y procesar el archivo de entrada
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                contenido = f.read()
                # Separar por espacios y saltos de línea
                palabras = contenido.split()
                
                # Analizar cada palabra
                for palabra in palabras:
                    tipo_token, lexema = self.clasificar_token(palabra)
                    tokens.append((tipo_token, lexema))
            
            # Generar archivo de salida
            self.generar_salida(tokens, archivo_salida)
            
            print(f"\nAnálisis completado: {len(tokens)} tokens procesados")
            print(f"Resultados guardados en: {archivo_salida}")
            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo_entrada}")
            raise
        except Exception as e:
            print(f"Error al analizar el archivo: {e}")
            raise
    
    def generar_salida(self, tokens, archivo_salida):
        """
        Genera el archivo de salida en formato de tabla.
        
        Args:
            tokens: Lista de tuplas (tipo_token, lexema)
            archivo_salida: Ruta al archivo de salida
        """
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                # Escribir encabezado
                f.write(f"{'Token':<20} {'Lexema':<20}\n")
                f.write("-" * 40 + "\n")
                
                # Escribir cada token
                for tipo_token, lexema in tokens:
                    f.write(f"{tipo_token:<20} {lexema:<20}\n")
                
            # Mostrar también en consola
            print("\n" + "=" * 40)
            print(f"{'Token':<20} {'Lexema':<20}")
            print("=" * 40)
            for tipo_token, lexema in tokens:
                print(f"{tipo_token:<20} {lexema:<20}")
            print("=" * 40)
            
        except Exception as e:
            print(f"Error al generar el archivo de salida: {e}")
            raise


def main():
    """
    Función principal del programa.
    """
    print("=" * 50)
    print("ANALIZADOR LÉXICO - LENGUAJES Y AUTÓMATAS")
    print("Universidad Politécnica de Chiapas")
    print("=" * 50)
    
    # Archivos de entrada y salida
    archivo_diccionario = "diccionario.txt"
    archivo_entrada = "texto_entrada.txt"
    archivo_salida = "tokens_salida.txt"
    
    try:
        # Crear instancia del analizador léxico
        analizador = AnalizadorLexico(archivo_diccionario)
        
        # Analizar el archivo de entrada
        analizador.analizar_archivo(archivo_entrada, archivo_salida)
        
        print("\n✓ Proceso completado exitosamente")
        
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
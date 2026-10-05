import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Locale;

/**
 * Programa principal que crea datos de ejemplo, ejecuta el modelo de lluvia
 * y muestra los resultados en consola.
 */
public class Main {

    /**
    * Imprime la tabla de resultados.
     */
    public static void main(String[] args) throws IOException {
        DatosMeteorologicos[] datos = cargarDatos();
        ModeloLluvia modelo = new ModeloLluvia();

        System.out.println("\nRESULTADOS");
        System.out.println("Hora     Hum.   Nub.   Temp.      H      N     Tf        I  Estado");
        System.out.println("-----------------------------------------------------------------------");

        for (DatosMeteorologicos dato : datos) {
            ResultadoSimulacion resultado = modelo.evaluar(dato);

            System.out.printf(
                Locale.US,
                "%-8s %5.0f %6.0f %7.1f %7.2f %7.2f %7.2f %8.3f  %s%n",
                dato.getHora(),
                dato.getHumedad(),
                dato.getNubosidad(),
                dato.getTemperatura(),
                resultado.getH(),
                resultado.getN(),
                resultado.getTf(),
                resultado.getIndice(),
                resultado.getEstado()
            );
        }
    }

    private static DatosMeteorologicos[] cargarDatos() throws IOException {
        List<String> filas = Files.readAllLines(
                Paths.get("python", "datos.csv"), StandardCharsets.UTF_8);
        DatosMeteorologicos[] datos = new DatosMeteorologicos[filas.size() - 1];

        for (int i = 1; i < filas.size(); i++) {
            String[] valores = filas.get(i).split(",");
            datos[i - 1] = new DatosMeteorologicos(
                    valores[0],
                    Double.parseDouble(valores[1]),
                    Double.parseDouble(valores[2]),
                    Double.parseDouble(valores[3])
            );
        }

        return datos;
    }
}

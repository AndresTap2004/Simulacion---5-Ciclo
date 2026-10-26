import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Ejecuta el modelo de lluvia, ajusta el índice y exporta tablas y una gráfica.
 */
public class Main {

    public static void main(String[] args) throws IOException {
        DatosMeteorologicos[] datos = cargarDatos();
        ModeloLluvia modelo = new ModeloLluvia();
        List<ResultadoSimulacion> resultados = new ArrayList<>();

        System.out.println("\nRESULTADOS");
        System.out.println("Hora     Hum.   Nub.   Temp.      H      N     Tf        I  Estado");
        System.out.println("-----------------------------------------------------------------------");

        for (DatosMeteorologicos dato : datos) {
            ResultadoSimulacion resultado = modelo.evaluar(dato);
            resultados.add(resultado);

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

        AjusteExponencial.ResultadoAjuste ajuste =
                new AjusteExponencial().ajustar(resultados);
        System.out.println("\nTABLA DEL MODELO EXPONENCIAL AJUSTADO");
        System.out.println(
                "Hora     Humr   Nub.   Temp.      H      N     Tf"
                        + " I original I ajustado        Tendencia  Estado");
        System.out.println(
                "--------------------------------------------------------------------------"
                        + "-----------------------------");
        for (AjusteExponencial.PuntoAjustado punto : ajuste.getPuntos()) {
            System.out.printf(
                    Locale.US,
                    "%-8s %5.0f %6.0f %7.1f %6.2f %6.2f %6.2f"
                            + " %10.3f %11.3f %16s  %s%n",
                    punto.getHora(),
                    punto.getHumedad(),
                    punto.getNubosidad(),
                    punto.getTemperatura(),
                    punto.getH(),
                    punto.getN(),
                    punto.getTf(),
                    punto.getIndiceOriginal(),
                    punto.getIndiceAjustado(),
                    punto.getTendencia(),
                    punto.getEstado()
            );
        }
        System.out.printf(
                Locale.US,
                "%nP0 = %.3f; r crecimiento = %.6f h^-1; "
                        + "r decrecimiento = %.6f h^-1%n",
                ajuste.getP0(),
                ajuste.getTasaCrecimiento(),
                ajuste.getTasaDecrecimiento()
        );

        Path salida = Paths.get("java", "output");
        Files.createDirectories(salida);
        exportarResultados(salida.resolve("resultados.csv"), resultados);
        exportarAjuste(salida.resolve("ajuste_exponencial.csv"), ajuste);
        new GraficasSvg().generar(
                salida.resolve("ajuste_exponencial.svg"), ajuste.getPuntos());
        System.out.println(
                "Archivos generados en java/output/: resultados.csv, "
                        + "ajuste_exponencial.csv y ajuste_exponencial.svg");
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

    private static void exportarResultados(
            Path destino, List<ResultadoSimulacion> resultados) throws IOException {
        StringBuilder csv = new StringBuilder(
                "hora,humedad,nubosidad,temperatura,H,N,Tf,indice,estado\n");
        for (ResultadoSimulacion resultado : resultados) {
            DatosMeteorologicos dato = resultado.getDatos();
            csv.append(String.format(
                    Locale.US,
                    "%s,%.0f,%.0f,%.1f,%.2f,%.2f,%.2f,%.3f,%s%n",
                    dato.getHora(),
                    dato.getHumedad(),
                    dato.getNubosidad(),
                    dato.getTemperatura(),
                    resultado.getH(),
                    resultado.getN(),
                    resultado.getTf(),
                    resultado.getIndice(),
                    resultado.getEstado()
            ));
        }
        Files.write(destino, csv.toString().getBytes(StandardCharsets.UTF_8));
    }

    private static void exportarAjuste(
            Path destino, AjusteExponencial.ResultadoAjuste ajuste)
            throws IOException {
        StringBuilder csv = new StringBuilder(
                "hora,humedad,nubosidad,temperatura,H,N,Tf,indice_original,"
                        + "indice_ajustado,tendencia,r_por_hora,estado\n");
        for (AjusteExponencial.PuntoAjustado punto : ajuste.getPuntos()) {
            csv.append(String.format(
                    Locale.US,
                    "%s,%.0f,%.0f,%.1f,%.2f,%.2f,%.2f,%.3f,%.3f,%s,%.6f,%s%n",
                    punto.getHora(),
                    punto.getHumedad(),
                    punto.getNubosidad(),
                    punto.getTemperatura(),
                    punto.getH(),
                    punto.getN(),
                    punto.getTf(),
                    punto.getIndiceOriginal(),
                    punto.getIndiceAjustado(),
                    punto.getTendencia(),
                    punto.getTasa(),
                    punto.getEstado()
            ));
        }
        Files.write(destino, csv.toString().getBytes(StandardCharsets.UTF_8));
    }
}

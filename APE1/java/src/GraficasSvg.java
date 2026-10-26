import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Genera una gráfica SVG sin dependencias externas. */
public class GraficasSvg {
    private static final int ANCHO = 900;
    private static final int ALTO = 520;
    private static final int IZQUIERDA = 75;
    private static final int ARRIBA = 35;
    private static final int ANCHO_GRAFICA = 770;
    private static final int ALTO_GRAFICA = 400;

    public void generar(Path destino,
                        List<AjusteExponencial.PuntoAjustado> puntos) throws IOException {
        if (puntos.size() < 2) {
            throw new IllegalArgumentException(
                    "Se requieren al menos dos puntos para generar la gráfica.");
        }

        Files.createDirectories(destino.getParent());
        double horaInicial = horaEnHoras(puntos.get(0).getHora());
        double horaFinal = horaEnHoras(puntos.get(puntos.size() - 1).getHora());
        if (horaFinal <= horaInicial) {
            throw new IllegalArgumentException("El rango horario no es válido.");
        }

        StringBuilder svg = new StringBuilder();
        svg.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            .append("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"")
            .append(ANCHO).append("\" height=\"").append(ALTO)
            .append("\" viewBox=\"0 0 ").append(ANCHO).append(' ')
            .append(ALTO).append("\">\n")
            .append("<rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n")
            .append("<text x=\"450\" y=\"24\" text-anchor=\"middle\" ")
            .append("font-family=\"Arial\" font-size=\"18\">")
            .append("Ajuste exponencial del índice de lluvia</text>\n");

        banda(svg, 0.0, 0.40, "#dcefe5");
        banda(svg, 0.40, 0.60, "#fff0c2");
        banda(svg, 0.60, 0.75, "#ffdfbf");
        banda(svg, 0.75, 1.00, "#f5dada");

        for (double umbral : new double[]{0.40, 0.60, 0.75}) {
            double y = coordenadaY(umbral);
            svg.append("<line x1=\"").append(IZQUIERDA).append("\" y1=\"")
                .append(y).append("\" x2=\"")
                .append(IZQUIERDA + ANCHO_GRAFICA).append("\" y2=\"")
                .append(y).append("\" stroke=\"#59636e\" stroke-dasharray=\"6 5\"/>")
                .append("<text x=\"").append(IZQUIERDA + ANCHO_GRAFICA + 6)
                .append("\" y=\"").append(y + 4)
                .append("\" font-family=\"Arial\" font-size=\"12\">")
                .append(String.format(java.util.Locale.US, "%.2f", umbral))
                .append("</text>\n");
        }

        puntos(svg, puntos, horaInicial, horaFinal, "indiceOriginal",
                "#68737d", "5 4", "Índice calculado", 0, puntos.size());
        int maximo = 0;
        for (int i = 1; i < puntos.size(); i++) {
            if (puntos.get(i).getIndiceOriginal()
                    > puntos.get(maximo).getIndiceOriginal()) {
                maximo = i;
            }
        }
        puntos(svg, puntos, horaInicial, horaFinal, "indiceAjustado",
                "#18794e", "", "Crecimiento exponencial", 0, maximo + 1);
        puntos(svg, puntos, horaInicial, horaFinal, "indiceAjustado",
                "#bf3f3f", "", "Decrecimiento exponencial", maximo,
                puntos.size());

        svg.append("<line x1=\"").append(IZQUIERDA).append("\" y1=\"")
            .append(ARRIBA).append("\" x2=\"").append(IZQUIERDA)
            .append("\" y2=\"").append(ARRIBA + ALTO_GRAFICA)
            .append("\" stroke=\"#333\"/><line x1=\"").append(IZQUIERDA)
            .append("\" y1=\"").append(ARRIBA + ALTO_GRAFICA)
            .append("\" x2=\"").append(IZQUIERDA + ANCHO_GRAFICA)
            .append("\" y2=\"").append(ARRIBA + ALTO_GRAFICA)
            .append("\" stroke=\"#333\"/>\n");

        for (AjusteExponencial.PuntoAjustado punto : puntos) {
            double hora = horaEnHoras(punto.getHora());
            double x = coordenadaX(hora, horaInicial, horaFinal);
            svg.append("<text x=\"").append(x).append("\" y=\"")
                .append(ARRIBA + ALTO_GRAFICA + 22)
                .append("\" text-anchor=\"middle\" font-family=\"Arial\" ")
                .append("font-size=\"12\">").append(punto.getHora())
                .append("</text>\n");
        }

        svg.append("<text x=\"460\" y=\"505\" text-anchor=\"middle\" ")
            .append("font-family=\"Arial\" font-size=\"14\">Hora</text>\n")
            .append("<text x=\"18\" y=\"235\" text-anchor=\"middle\" ")
            .append("font-family=\"Arial\" font-size=\"14\" ")
            .append("transform=\"rotate(-90 18 235)\">Índice I</text>\n");
        leyenda(svg, 76, 55, "#68737d", "Índice calculado");
        leyenda(svg, 250, 55, "#18794e", "Crecimiento exponencial");
        leyenda(svg, 470, 55, "#bf3f3f", "Decrecimiento exponencial");
        svg.append("</svg>\n");
        Files.write(destino, svg.toString().getBytes(StandardCharsets.UTF_8));
    }

    private static void banda(StringBuilder svg, double inferior, double superior,
                              String color) {
        double y = coordenadaY(superior);
        double alto = coordenadaY(inferior) - y;
        svg.append("<rect x=\"").append(IZQUIERDA).append("\" y=\"").append(y)
            .append("\" width=\"").append(ANCHO_GRAFICA).append("\" height=\"")
            .append(alto).append("\" fill=\"").append(color)
            .append("\" opacity=\"0.7\"/>\n");
    }

    private static void puntos(StringBuilder svg,
                               List<AjusteExponencial.PuntoAjustado> puntos,
                               double horaInicial, double horaFinal,
                               String campo, String color, String dash,
                               String etiqueta, int inicio, int fin) {
        StringBuilder coordenadas = new StringBuilder();
        for (int i = inicio; i < fin; i++) {
            AjusteExponencial.PuntoAjustado punto = puntos.get(i);
            double valor = campo.equals("indiceOriginal")
                    ? punto.getIndiceOriginal() : punto.getIndiceAjustado();
            coordenadas.append(coordenadaX(
                    horaEnHoras(punto.getHora()), horaInicial, horaFinal))
                .append(',').append(coordenadaY(valor)).append(' ');
        }
        svg.append("<polyline fill=\"none\" stroke=\"").append(color)
            .append("\" stroke-width=\"2.5\"");
        if (!dash.isEmpty()) {
            svg.append(" stroke-dasharray=\"").append(dash).append("\"");
        }
        svg.append(" points=\"").append(coordenadas).append("\"/>\n");
        for (int i = inicio; i < fin; i++) {
            AjusteExponencial.PuntoAjustado punto = puntos.get(i);
            double valor = campo.equals("indiceOriginal")
                    ? punto.getIndiceOriginal() : punto.getIndiceAjustado();
            svg.append("<circle cx=\"")
                .append(coordenadaX(horaEnHoras(punto.getHora()),
                        horaInicial, horaFinal))
                .append("\" cy=\"").append(coordenadaY(valor))
                .append("\" r=\"4\" fill=\"").append(color)
                .append("\"/>\n");
        }
    }

    private static void leyenda(StringBuilder svg, int x, int y,
                                String color, String texto) {
        svg.append("<line x1=\"").append(x).append("\" y1=\"").append(y)
            .append("\" x2=\"").append(x + 24).append("\" y2=\"").append(y)
            .append("\" stroke=\"").append(color)
            .append("\" stroke-width=\"3\"/><text x=\"").append(x + 30)
            .append("\" y=\"").append(y + 4)
            .append("\" font-family=\"Arial\" font-size=\"12\">")
            .append(texto).append("</text>\n");
    }

    private static double coordenadaX(double hora, double inicial, double finalHora) {
        return IZQUIERDA + (hora - inicial) / (finalHora - inicial) * ANCHO_GRAFICA;
    }

    private static double coordenadaY(double indice) {
        return ARRIBA + (1.0 - indice) * ALTO_GRAFICA;
    }

    private static double horaEnHoras(String hora) {
        String[] partes = hora.split(":");
        return Integer.parseInt(partes[0]) + Integer.parseInt(partes[1]) / 60.0;
    }
}

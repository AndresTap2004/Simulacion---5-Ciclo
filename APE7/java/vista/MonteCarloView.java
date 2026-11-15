package vista;

import controlador.MonteCarloController;

import javax.imageio.ImageIO;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Stroke;
import java.awt.image.BufferedImage;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

public class MonteCarloView {
    private static final int ANCHO = 1350;
    private static final int ALTO = 1050;
    private static final Color AZUL = new Color(40, 105, 175);
    private static final Color NARANJA = new Color(230, 125, 35);
    private static final Color ROJO = new Color(190, 55, 55);
    private static final double PI = Math.PI;

    public void mostrarResultados(MonteCarloController.ResultadoSimulacion[] resultados) {
        System.out.println("==========================================================================");
        System.out.println(" N          | Pi Estimado      | Error Absoluto   | Tiempo Java (ms)     ");
        System.out.println("==========================================================================");

        for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
            System.out.printf("%-11d | %-16.6f | %-16.6f | %-20d%n",
                    resultado.getN(),
                    resultado.getPiEstimado(),
                    resultado.getErrorAbsoluto(),
                    resultado.getTiempoMs());
        }
        System.out.println("==========================================================================");
    }

    public Path guardarResultadosCsv(
            MonteCarloController.ResultadoSimulacion[] resultados,
            Path archivoCsv) throws IOException {
        Path directorio = archivoCsv.getParent();
        if (directorio != null) {
            Files.createDirectories(directorio);
        }

        try (BufferedWriter escritor = Files.newBufferedWriter(archivoCsv, StandardCharsets.UTF_8)) {
            escritor.write("n,pi_estimado,error_absoluto,tiempo_ms");
            escritor.newLine();
            for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
                escritor.write(String.format(
                        Locale.ROOT,
                        "%d,%.15f,%.15f,%d",
                        resultado.getN(),
                        resultado.getPiEstimado(),
                        resultado.getErrorAbsoluto(),
                        resultado.getTiempoMs()));
                escritor.newLine();
            }
        }
        return archivoCsv;
    }

    public Path generarGraficaConvergencia(
            MonteCarloController.ResultadoSimulacion[] resultados,
            Path directorioSalida) throws IOException {
        if (resultados == null || resultados.length == 0) {
            throw new IllegalArgumentException("Se requieren resultados Java para generar la gráfica.");
        }

        Files.createDirectories(directorioSalida);
        Path archivo = directorioSalida.resolve("convergencia_java.png");
        BufferedImage imagen = new BufferedImage(ANCHO, ALTO, BufferedImage.TYPE_INT_RGB);
        Graphics2D graficos = imagen.createGraphics();
        try {
            graficos.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graficos.setColor(Color.WHITE);
            graficos.fillRect(0, 0, ANCHO, ALTO);
            graficos.setColor(Color.BLACK);
            graficos.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 24));
            dibujarTextoCentrado(graficos, "Convergencia de Monte Carlo - Java", ANCHO / 2, 38);

            dibujarPanel(graficos, resultados, 55, 430, false);
            dibujarPanel(graficos, resultados, 510, 430, true);
        } finally {
            graficos.dispose();
        }

        ImageIO.write(imagen, "png", archivo.toFile());
        return archivo;
    }

    private void dibujarPanel(
            Graphics2D graficos,
            MonteCarloController.ResultadoSimulacion[] resultados,
            int inicioY,
            int altoPanel,
            boolean mostrarError) {
        int izquierda = 120;
        int derecha = ANCHO - 20;
        int arriba = inicioY + 45;
        int abajo = inicioY + altoPanel - 75;
        int anchoGrafica = derecha - izquierda;
        int altoGrafica = abajo - arriba;

        double minimoX = Math.log10(resultados[0].getN());
        double maximoX = Math.log10(resultados[resultados.length - 1].getN());
        double margenX = (maximoX - minimoX) * 0.05;
        minimoX -= margenX;
        maximoX += margenX;
        double minimoY = mostrarError ? 0.0 : PI;
        double maximoY = mostrarError ? 0.0 : PI;
        for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
            double valor = mostrarError ? resultado.getErrorAbsoluto() : resultado.getPiEstimado();
            minimoY = Math.min(minimoY, valor);
            maximoY = Math.max(maximoY, valor);
        }
        double margen = Math.max((maximoY - minimoY) * 0.05, mostrarError ? 0.000001 : 0.0005);
        minimoY = mostrarError ? 0.0 : minimoY - margen;
        maximoY += margen;

        graficos.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 20));
        graficos.setColor(Color.BLACK);
        dibujarTextoCentrado(
                graficos,
                mostrarError ? "Error absoluto" : "Estimación de π",
                (izquierda + derecha) / 2,
                inicioY + 22);

        graficos.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 15));
        DecimalFormat formato = new DecimalFormat(
                "0.000000",
                DecimalFormatSymbols.getInstance(Locale.ROOT));
        for (int marca = 0; marca <= 5; marca++) {
            int y = abajo - marca * altoGrafica / 5;
            double valor = minimoY + (maximoY - minimoY) * marca / 5.0;
            graficos.setColor(new Color(225, 225, 225));
            graficos.drawLine(izquierda, y, derecha, y);
            graficos.setColor(Color.DARK_GRAY);
            String etiqueta = formato.format(valor);
            graficos.drawString(etiqueta, izquierda - graficos.getFontMetrics().stringWidth(etiqueta) - 10, y + 5);
        }

        graficos.setColor(new Color(225, 225, 225));
        for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
            int x = transformarX(resultado.getN(), minimoX, maximoX, izquierda, anchoGrafica);
            graficos.drawLine(x, arriba, x, abajo);
        }

        graficos.setColor(Color.DARK_GRAY);
        graficos.drawLine(izquierda, arriba, izquierda, abajo);
        graficos.drawLine(izquierda, abajo, derecha, abajo);
        dibujarTextoCentrado(graficos, "Número de puntos (N)", (izquierda + derecha) / 2, abajo + 55);

        if (!mostrarError) {
            Stroke trazoAnterior = graficos.getStroke();
            graficos.setColor(ROJO);
            graficos.setStroke(new BasicStroke(2, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL, 0, new float[]{8, 6}, 0));
            int yPi = transformarY(PI, minimoY, maximoY, arriba, altoGrafica);
            graficos.drawLine(izquierda, yPi, derecha, yPi);
            graficos.setStroke(trazoAnterior);
            dibujarLeyenda(graficos, derecha - 270, arriba + 12);
        }

        graficos.setColor(mostrarError ? NARANJA : AZUL);
        graficos.setStroke(new BasicStroke(2));
        int xAnterior = -1;
        int yAnterior = -1;
        for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
            int x = transformarX(resultado.getN(), minimoX, maximoX, izquierda, anchoGrafica);
            double valor = mostrarError ? resultado.getErrorAbsoluto() : resultado.getPiEstimado();
            int y = transformarY(valor, minimoY, maximoY, arriba, altoGrafica);

            if (xAnterior >= 0) {
                graficos.drawLine(xAnterior, yAnterior, x, y);
            }
            graficos.fillOval(x - 6, y - 6, 12, 12);

            String etiquetaN = String.format(Locale.ROOT, "%,d", resultado.getN());
            int anchoEtiqueta = graficos.getFontMetrics().stringWidth(etiquetaN);
            graficos.setColor(Color.DARK_GRAY);
            graficos.drawString(etiquetaN, x - anchoEtiqueta / 2, abajo + 22);
            graficos.setColor(mostrarError ? NARANJA : AZUL);
            xAnterior = x;
            yAnterior = y;
        }
    }

    private void dibujarLeyenda(Graphics2D graficos, int x, int y) {
        graficos.setColor(Color.WHITE);
        graficos.fillRoundRect(x, y, 250, 32, 6, 6);
        graficos.setColor(new Color(210, 210, 210));
        graficos.drawRoundRect(x, y, 250, 32, 6, 6);
        graficos.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 16));
        graficos.setColor(AZUL);
        graficos.drawLine(x + 12, y + 16, x + 40, y + 16);
        graficos.fillOval(x + 23, y + 11, 10, 10);
        graficos.setColor(Color.BLACK);
        graficos.drawString("π estimado", x + 48, y + 22);

        graficos.setColor(ROJO);
        Stroke trazoAnterior = graficos.getStroke();
        graficos.setStroke(new BasicStroke(2, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL, 0, new float[]{5, 4}, 0));
        graficos.drawLine(x + 145, y + 16, x + 171, y + 16);
        graficos.setStroke(trazoAnterior);
        graficos.setColor(Color.BLACK);
        graficos.drawString("π real", x + 178, y + 22);
    }

    private int transformarY(double valor, double minimo, double maximo, int arriba, int alto) {
        return arriba + (int) Math.round((maximo - valor) / (maximo - minimo) * alto);
    }

    private int transformarX(int valor, double minimo, double maximo, int izquierda, int ancho) {
        double logValor = Math.log10(valor);
        return maximo == minimo
                ? izquierda + ancho / 2
                : izquierda + (int) Math.round((logValor - minimo) / (maximo - minimo) * ancho);
    }

    private void dibujarTextoCentrado(Graphics2D graficos, String texto, int centroX, int y) {
        FontMetrics metricas = graficos.getFontMetrics();
        graficos.drawString(texto, centroX - metricas.stringWidth(texto) / 2, y);
    }
}

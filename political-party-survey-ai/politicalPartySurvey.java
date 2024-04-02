/*
 * A program that gathers survey responses in order to predict political party
 * using very basic AI training
 * Written by Huy Lam
 */

import java.util.Scanner;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class politicalPartySurvey {
    static String currentDir = (System.getProperty("user.dir") + "/political-party-survey-ai");

    public static void main(String[] args) {
        // initialize scanner and scope of survey
        Scanner scanner = new Scanner(System.in);
        int questionMax = 5;
        int choiceMax = 4;

        // answers array has final values, tempAnswers to calculate with
        int[][] answers = new int[questionMax][choiceMax];
        int[][] tempAnswers = new int[questionMax][choiceMax];
        String partyAnswer = "";

        // create new files for answer storage if they do not exist
        File resourcesFolder = new File(currentDir + "/resources");
        if (!resourcesFolder.exists()) {
            resourcesFolder.mkdirs();
        }

        createPartyFile(currentDir + "/resources/republican.txt");
        createPartyFile(currentDir + "/resources/democratic.txt");
        createPartyFile(currentDir + "/resources/greenparty.txt");
        createPartyFile(currentDir + "/resources/libertarian.txt");

        // load up previous answers as one big 2D array
        int[][] previousAnswers = readPreviousIntoArray(questionMax, choiceMax);

        // build array of most popular answers
        int[][] mostPopular = new int[questionMax][choiceMax];

        // parse previousAnswers array to populate mostPopular array
        for (int row = 0; row < questionMax; row++) {
            for (int col = 0; col < choiceMax; col++) {
                int highestValue = 0;
                int highestParty = 0;
                for (int rowCount = row; rowCount < questionMax * 4; rowCount += questionMax) {
                    if (previousAnswers[rowCount][col] > highestValue) {
                        highestValue = previousAnswers[rowCount][col];
                        if (rowCount < questionMax) {
                            highestParty = 1;
                        } else if (rowCount < questionMax * 2) {
                            highestParty = 2;
                        } else if (rowCount < questionMax * 3) {
                            highestParty = 3;
                        } else {
                            highestParty = 4;
                        }
                    }
                    // store results in mostPopular array
                    mostPopular[row][col] = highestParty;
                }
            }
        }

        // begin survey
        clearScreen();
        System.out.println("Answer questions to determine your political leaning:");
        System.out.println("Valid reponses are A, B, C, or D.");
        System.out.println();

        // initiate variables to track predictions
        // boolean isRight = false;
        String partyGuess = "";
        List<String> guesses = new ArrayList<>(Arrays.asList("Republican", "Democratic", "Green Party", "Libertarian"));

        // display questions from displayQuestion function, storing answer to
        // tempAnswers
        for (int i = 1; i <= questionMax; i++) {
            clearScreen();
            System.out.println("Question " + i + "/" + questionMax + ": ");
            displayQuestion(i);
            System.out.print("Your answer: ");
            String answer = scanner.nextLine();
            System.out.println();

            if (answer.equals("A")) {
                tempAnswers[i - 1][0]++;
            }
            if (answer.equals("B")) {
                tempAnswers[i - 1][1]++;
            }
            if (answer.equals("C")) {
                tempAnswers[i - 1][2]++;
            }
            if (answer.equals("D")) {
                tempAnswers[i - 1][3]++;
            }

            // predict party unless insufficient data
            partyGuess = predictParty(answer, mostPopular, i);
            if (guesses.contains(partyGuess)) {
                clearScreen();
                System.out.print("Is your party " + partyGuess + "? (Y/N): ");
                String answer2 = scanner.nextLine();
                System.out.println();

                // if successful, save and exit
                if (answer2.equals("Y")) {
                    clearScreen();
                    partyAnswer = partyGuess;
                    saveAnswersToFile(answers, tempAnswers, questionMax, partyAnswer);
                    System.out.println("Prediction successful. Results saved.");
                    System.exit(0);
                    // else, remove guess from array
                } else {
                    guesses.remove(partyGuess);
                }
            }
        }

        // ask for party if there has been no (correct) prediction yet
        clearScreen();
        System.out.println("What party do you belong to?");
        System.out.println("A. Republican");
        System.out.println("B. Democratic");
        System.out.println("C. Green Party");
        System.out.println("D. Libertarian");
        System.out.print("Your answer: ");
        String answer = scanner.nextLine();

        // store results to appropriate party text file to load up next time survey is
        // run
        if (answer.equals("A")) {
            partyAnswer = "republican";
        }
        if (answer.equals("B")) {
            partyAnswer = "democratic";
        }
        if (answer.equals("C")) {
            partyAnswer = "greenparty";
        }
        if (answer.equals("D")) {
            partyAnswer = "libertarian";
        }
        System.out.println();

        saveAnswersToFile(answers, tempAnswers, questionMax, partyAnswer);
        scanner.close();
    }

    // function to load up previous answers
    private static int[][] readPreviousIntoArray(Integer questionMax, Integer choiceMax) {
        // load previous answers into an array by reading all files
        int[][] previousAnswers = new int[questionMax * 4][choiceMax];
        String[] filenames = { currentDir + "/resources/republican.txt", currentDir + "/resources/democratic.txt",
                currentDir + "/resources/greenparty.txt", currentDir + "/resources/libertarian.txt" };

        // parse files and load into array
        for (int partyIndex = 0; partyIndex < filenames.length; partyIndex++) {
            try {
                File file = new File(filenames[partyIndex]);
                Scanner scanner = new Scanner(file);

                int row = 0;
                while (scanner.hasNextLine() && row < 20) {
                    String line = scanner.nextLine();
                    String[] elements = line.split(" ");
                    for (int col = 0; col < elements.length && col < 4; col++) {
                        previousAnswers[row + (partyIndex * 5)][col] = Integer.parseInt(elements[col]);
                    }
                    row++;
                }
                scanner.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
        return previousAnswers;
    }

    // function to write answers to file
    private static void saveAnswersToFile(int[][] answers, int[][] tempAnswers, int questionMax, String partyAnswer) {
        // initialize variables
        String fileName = currentDir + "/resources/" + partyAnswer + ".txt";
        int newValue = 0;

        // read party's text file into answers array
        try {
            File file = new File(fileName);
            Scanner scanner = new Scanner(file);

            int row = 0;
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] elements = line.split(" ");
                for (int col = 0; col < elements.length; col++) {
                    answers[row][col] = Integer.parseInt(elements[col]);
                }
                row++;
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        // add answers and tempAnswers and write to party's text file
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int i = 0; i < answers.length; i++) {
                for (int j = 0; j < answers[i].length; j++) {
                    newValue = answers[i][j] + tempAnswers[i][j];
                    writer.write(newValue + " ");
                }
                writer.newLine();
            }

        } catch (IOException e) {
            System.out.println("An error occurred while saving the survey responses.");
            e.printStackTrace();
        }
    }

    // function to predict user's political party
    private static String predictParty(String answer, int[][] mostPopular, int questionNumber) {
        // array of possible guesses
        String partyGuess = "";
        int answerCol = 0;

        // correspond answer to column number to see most popular party that chose that
        // answer
        if (answer.equals("A")) {
            answerCol = 0;
        }
        if (answer.equals("B")) {
            answerCol = 1;
        }
        if (answer.equals("C")) {
            answerCol = 2;
        }
        if (answer.equals("D")) {
            answerCol = 3;
        }

        // int to string conversions
        int partyGuessInt = mostPopular[questionNumber - 1][answerCol];

        if (partyGuessInt == 1) {
            partyGuess = "Republican";
        }
        if (partyGuessInt == 2) {
            partyGuess = "Democratic";
        }
        if (partyGuessInt == 3) {
            partyGuess = "Green Party";
        }
        if (partyGuessInt == 4) {
            partyGuess = "Libertarian";
        }

        return partyGuess;
    }

    // function to create text files if they do not exist
    private static void createPartyFile(String filename) {
        File file = new File(filename);
        try {
            file.createNewFile();
        } catch (IOException e) {
            System.out.println("An error occurred while creating the file: " + filename);
            e.printStackTrace();
        }
    }

    // function to store and call on questions
    private static void displayQuestion(int questionNumber) {
        switch (questionNumber) {
            case 1:
                System.out.println("What is your stance on gun control?");
                System.out.println("A. Support stricter gun control measures.");
                System.out.println("B. Support the Second Amendment rights without major restrictions.");
                System.out.println("C. Advocate for complete disarmament.");
                System.out.println("D. Believe in minimal government intervention in gun ownership.");
                break;
            case 2:
                System.out.println("How do you feel about tax policies?");
                System.out.println("A. Support higher taxes for the wealthy to fund social programs.");
                System.out.println("B. Support lower taxes across the board to stimulate the economy.");
                System.out.println("C. Support a wealth tax to reduce income inequality.");
                System.out.println("D. Advocate for minimal government taxation and spending.");
                break;
            case 3:
                System.out.println("What is your view on climate change and environmental issues?");
                System.out.println("A. Strongly believe in taking immediate action to combat climate change.");
                System.out.println("B. Support balanced approaches that consider economic impacts as well.");
                System.out
                        .println("C. Advocate for radical changes to eliminate all pollution and protect ecosystems.");
                System.out.println(
                        "D. Believe that free markets and individual choices will naturally address environmental concerns.");
                break;
            case 4:
                System.out.println("What should be the government's role in healthcare?");
                System.out.println("A. Support a universal healthcare system.");
                System.out.println("B. Advocate for free-market competition and less government involvement.");
                System.out.println("C. Believe in a complete overhaul of the healthcare system.");
                System.out.println("D. Support minimal government intervention in healthcare.");
                break;
            case 5:
                System.out.println("How do you think immigration policies should be handled?");
                System.out.println("A. Support comprehensive immigration reform and pathways to citizenship.");
                System.out.println("B. Advocate for stricter border controls and immigration restrictions.");
                System.out.println("C. Believe in open borders and unrestricted immigration.");
                System.out.println("D. Support minimal government intervention in immigration.");
                break;
        }
    }

    public static void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}
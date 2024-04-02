/**
 * State Capitals Quiz
 *
 * This program quizzes the user on U.S. state capitals.
 * It displays the list of states and capitals,
 * bubble sorts the list by capital,
 * then quizes the user.
 * The total of correct answers are displayed at the end.
 *
 * Author: Huy Lam
 */

import java.util.Scanner;

public class stateCapitalsQuiz {
    public static void main(String[] args) {
        //store states and capitals in array
        String[][] stateCapitals = {
            {"Alabama", "Montgomery"},
            {"Alaska", "Juneau"},
            {"Arizona", "Phoenix"},
            {"Arkansas", "Little Rock"},
            {"California", "Sacramento"},
            {"Colorado", "Denver"},
            {"Connecticut", "Hartford"},
            {"Delaware", "Dover"},
            {"Florida", "Tallahassee"},
            {"Georgia", "Atlanta"},
            {"Hawaii", "Honolulu"},
            {"Idaho", "Boise"},
            {"Illinois", "Springfield"},
            {"Indiana", "Indianapolis"},
            {"Iowa", "Des Moines"},
            {"Kansas", "Topeka"},
            {"Kentucky", "Frankfort"},
            {"Louisiana", "Baton Rouge"},
            {"Maine", "Augusta"},
            {"Maryland", "Annapolis"},
            {"Massachusetts", "Boston"},
            {"Michigan", "Lansing"},
            {"Minnesota", "St. Paul"},
            {"Mississippi", "Jackson"},
            {"Missouri", "Jefferson City"},
            {"Montana", "Helena"},
            {"Nebraska", "Lincoln"},
            {"Nevada", "Carson City"},
            {"New Hampshire", "Concord"},
            {"New Jersey", "Trenton"},
            {"New Mexico", "Santa Fe"},
            {"New York", "Albany"},
            {"North Carolina", "Raleigh"},
            {"North Dakota", "Bismarck"},
            {"Ohio", "Columbus"},
            {"Oklahoma", "Oklahoma City"},
            {"Oregon", "Salem"},
            {"Pennsylvania", "Harrisburg"},
            {"Rhode Island", "Providence"},
            {"South Carolina", "Columbia"},
            {"South Dakota", "Pierre"},
            {"Tennessee", "Nashville"},
            {"Texas", "Austin"},
            {"Utah", "Salt Lake City"},
            {"Vermont", "Montpelier"},
            {"Virginia", "Richmond"},
            {"Washington", "Olympia"},
            {"West Virginia", "Charleston"},
            {"Wisconsin", "Madison"},
            {"Wyoming", "Cheyenne"}
        };

        //print entire array
        // System.out.println("States and capitals:");
        // //iterate through each key:value pair and print key (index 0 in pair) and value (index 1 in pair)
        // for (String[] state : stateCapitals) {
        //     System.out.println(state[0] + " - " + state[1]);
        // }
        // System.out.println();

        //bubble sort array by capital
        //iterate through entire array
        for (int i = 0; i < stateCapitals.length - 1; i++) {
            //within the array, compare current index to unsorted elements
            for (int j = 0; j < stateCapitals.length - i - 1; j++) {
                //compare the capital of current index to next index via alphabet ordering
                if (stateCapitals[j][1].compareToIgnoreCase(stateCapitals[j + 1][1]) > 0) {
                    //swap using temp as placeholder
                    String[] temp = stateCapitals[j];
                    stateCapitals[j] = stateCapitals[j + 1];
                    stateCapitals[j + 1] = temp;
                }
            }
        }

        //initialize scanner and correct answers count for quiz
        Scanner scanner = new Scanner(System.in);
        int correctCount = 0;

        //iterate over sorted array
        for (String[] state : stateCapitals) {
            //prompt user to enter capital of current state
            System.out.print("Enter the capital of " + state[0] + ": ");
            String userAnswer = scanner.nextLine();
            //if user is correct, notify and increase count, else just notify
            if (userAnswer.equalsIgnoreCase(state[1])) {
                correctCount++;
                System.out.println("Correct!");
            } else {
                System.out.println("Wrong.");
            }
        }

        //print out user results
        System.out.println("Total correct: " + correctCount);

        scanner.close();
    }
}
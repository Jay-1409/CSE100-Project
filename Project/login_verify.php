<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Assuming this is the login or signup page
    $username = $_POST["username"];
    $password = $_POST["password"];

    if (!empty($username) && !empty($password)) {
        // Check if the file exists
        $file = "credentials.csv";

        if (file_exists($file)) {
            $handle = fopen($file, "r");

            // Check if the file was opened successfully
            if ($handle) {
                $valid = false;

                // Check each row for login or signup
                while (($row = fgetcsv($handle)) !== false) {
                    if ($_POST["action"] === "login" && $row[0] === $username && $row[1] === $password) {
                        $valid = true;
                        break;
                    } elseif ($_POST["action"] === "signup" && $row[0] === $username) {
                        $valid = false; // Username already exists for signup
                        break;
                    }
                }

                fclose($handle);

                if ($_POST["action"] === "login") {
                    if ($valid) {
                        // Redirect to the home page or another page after successful login
                        header("Location: /home.html");
                        exit;
                    } else {
                        echo "Invalid username or password";
                    }
                } elseif ($_POST["action"] === "signup") {
                    if (!$valid) {
                        // Open the CSV file in append mode
                        $handle = fopen($file, "a");

                        // Check if the file was opened successfully
                        if ($handle) {
                            // Write the new user's information to the file
                            fputcsv($handle, [$username, $password]);

                            // Close the file
                            fclose($handle);

                            // Redirect to the home page or another page after successful signup
                            header("Location: /home.html");
                            exit;
                        } else {
                            echo "Error opening file for writing";
                        }
                    } else {
                        echo "Username already exists";
                    }
                }
            } else {
                echo "Error opening file for reading";
            }
        } else {
            echo "Credentials file not found";
        }
    } else {
        echo "Username or password is empty";
    }

?>

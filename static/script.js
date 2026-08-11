// ==========================================================
// GET HTML ELEMENTS
// ==========================================================

const password =
    document.getElementById("password");

const inputText =
    document.getElementById("inputText");

const outputText =
    document.getElementById("outputText");

const inputCount =
    document.getElementById("inputCount");

const outputCount =
    document.getElementById("outputCount");

const operationStatus =
    document.getElementById("operationStatus");

const statusText =
    document.getElementById("statusText");


// ==========================================================
// CHARACTER COUNTER
// ==========================================================

function updateCounters() {

    inputCount.textContent =
        inputText.value.length;

    outputCount.textContent =
        outputText.value.length;
}


// ==========================================================
// STATUS
// ==========================================================

function setStatus(message, success = true) {

    operationStatus.textContent =
        "STATUS: " + message;

    operationStatus.className =
        success ? "success" : "error";

    statusText.textContent =
        success ? "SECURE" : "ERROR";

    statusText.className =
        success ? "success" : "error";
}


// ==========================================================
// SHOW / HIDE PASSWORD
// ==========================================================

document
    .getElementById("togglePassword")
    .addEventListener("click", function () {

        if (password.type === "password") {

            password.type = "text";

            this.textContent = "HIDE";

        } else {

            password.type = "password";

            this.textContent = "SHOW";

        }

    });


// ==========================================================
// INPUT COUNTER
// ==========================================================

inputText.addEventListener(
    "input",
    updateCounters
);


// ==========================================================
// ENCRYPT
// ==========================================================

document
    .getElementById("encryptBtn")
    .addEventListener("click", async () => {

        const text =
            inputText.value.trim();

        const pass =
            password.value;


        // Check password

        if (!pass) {

            setStatus(
                "PASSWORD REQUIRED",
                false
            );

            return;
        }


        // Check input

        if (!text) {

            setStatus(
                "TEXT REQUIRED",
                false
            );

            return;
        }


        setStatus(
            "ENCRYPTING..."
        );


        try {

            const response =
                await fetch(
                    "/encrypt",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                text: text,
                                password: pass
                            })
                    }
                );


            const result =
                await response.json();


            if (
                !response.ok ||
                !result.success
            ) {

                throw new Error(
                    result.message
                );

            }


            // Display encrypted package

            outputText.value =
`Encrypted Text:
${result.encrypted_text}

IV:
${result.iv}

Salt:
${result.salt}`;


            updateCounters();


            setStatus(
                "ENCRYPTION SUCCESSFUL | AES-256 CBC"
            );


        } catch (error) {

            setStatus(
                error.message ||
                "ENCRYPTION FAILED",
                false
            );

        }

    });


// ==========================================================
// DECRYPT
// ==========================================================

document
    .getElementById("decryptBtn")
    .addEventListener("click", async () => {

        const data =
            inputText.value.trim();

        const pass =
            password.value;


        if (!pass) {

            setStatus(
                "PASSWORD REQUIRED",
                false
            );

            return;
        }


        if (!data) {

            setStatus(
                "ENCRYPTED DATA REQUIRED",
                false
            );

            return;
        }


        // Variables

        let encryptedText = "";

        let iv = "";

        let salt = "";

        let section = "";


        // Parse encrypted package

        data
            .split(/\r?\n/)
            .forEach(line => {

                line = line.trim();


                if (
                    line ===
                    "Encrypted Text:"
                ) {

                    section = "encrypted";

                }


                else if (
                    line === "IV:"
                ) {

                    section = "iv";

                }


                else if (
                    line === "Salt:"
                ) {

                    section = "salt";

                }


                else if (line) {

                    if (
                        section ===
                        "encrypted"
                    ) {

                        encryptedText += line;

                    }


                    if (
                        section === "iv"
                    ) {

                        iv += line;

                    }


                    if (
                        section === "salt"
                    ) {

                        salt += line;

                    }

                }

            });


        // Validate

        if (
            !encryptedText ||
            !iv ||
            !salt
        ) {

            setStatus(
                "INVALID ENCRYPTED DATA FORMAT",
                false
            );

            return;
        }


        setStatus(
            "DECRYPTING..."
        );


        try {

            const response =
                await fetch(
                    "/decrypt",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                encrypted_text:
                                    encryptedText,

                                iv:
                                    iv,

                                salt:
                                    salt,

                                password:
                                    pass

                            })
                    }
                );


            const result =
                await response.json();


            if (
                !response.ok ||
                !result.success
            ) {

                throw new Error(
                    result.message
                );

            }


            outputText.value =
                "DECRYPTED TEXT:\n\n" +
                result.decrypted_text;


            updateCounters();


            setStatus(
                "DECRYPTION SUCCESSFUL | AES-256 CBC"
            );


        } catch (error) {

            setStatus(
                error.message ||
                "DECRYPTION FAILED",
                false
            );

        }

    });


// ==========================================================
// CLEAR
// ==========================================================

document
    .getElementById("clearBtn")
    .addEventListener("click", () => {

        password.value = "";

        inputText.value = "";

        outputText.value = "";


        updateCounters();


        setStatus(
            "READY | Waiting for operation..."
        );


        password.type = "password";

        document
            .getElementById("togglePassword")
            .textContent = "SHOW";

    });


// ==========================================================
// COPY OUTPUT
// ==========================================================

document
    .getElementById("copyOutput")
    .addEventListener("click", async () => {

        if (!outputText.value) {

            setStatus(
                "NOTHING TO COPY",
                false
            );

            return;
        }


        try {

            await navigator.clipboard.writeText(
                outputText.value
            );


            setStatus(
                "OUTPUT COPIED TO CLIPBOARD"
            );


        } catch {

            setStatus(
                "COPY FAILED",
                false
            );

        }

    });


// ==========================================================
// INITIALIZE
// ==========================================================

updateCounters();

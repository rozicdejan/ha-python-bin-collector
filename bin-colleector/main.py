<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waste Collection Schedule</title>
    <style>
        /* Background animation */
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: white;
            font-size: 14px;
            margin-top: 10px;
        }

        .container {
            display: flex;
            justify-content: space-around;
            padding: 20px;
            flex-wrap: wrap;
        }

        .item {
            text-align: center;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            margin: 10px;
            flex: 1;
            min-width: 200px;
            max-width: 200px;
            transition: transform 0.3s;
        }

        .item:hover {
            transform: translateY(-10px);
        }

        .item img {
            width: 50px;
            height: 50px;
        }

        .item p {
            font-size: 14px;
            margin-top: 10px;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            position: fixed;
            width: 100%;
            bottom: 0;
            color: white;
            font-size: 0.8em;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }

            .item {
                padding: 15px;
                margin: 5px;
                min-width: 120px;
            }

            .item img {
                width: 40px;
                height: 40px;
            }
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>

<body>
    <div class="container">
        <div class="item" id="mko">
            <!-- Ensure the image exists in your static folder -->
            <img src="{{ url_for('static', filename='mesani.svg') }}" alt="Mešani komunalni odpadki">
            <p>{{ data.mko_name }}<br>{{ data.mko_date }}</p>
        </div>
        <div class="item" id="emb">
            <img src="{{ url_for('static', filename='embalaza.svg') }}" alt="Embalaža">
            <p>{{ data.emb_name }}<br>{{ data.emb_date }}</p>
        </div>
        <div class="item" id="bio">
            <img src="{{ url_for('static', filename='bioloski.svg') }}" alt="Biološki odpadki">
            <p>{{ data.bio_name }}<br>{{ data.bio_date }}</p>
        </div>
    </div>

    <script>
        // Auto-refresh every 15 seconds
        setInterval(function () {
            location.reload();
        }, 15000);
    </script>
</body>

</html>
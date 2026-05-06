# Pygame Platformer Game

A 2D platformer game built with **Pygame**, featuring smooth movement, animated sprites, and interactive level mechanics such as keys, doors, hazards, and moving platforms. The project follows a modular architecture for scalability and maintainability.

---

## Screenshots

<table>
  <tr>
    <td>
      <a href="https://ibb.co/JWNx0Dbc">
        <img src="https://i.ibb.co/TDZKp9nw/screenshot-2026-05-06-02-41-11.png" alt="screenshot-1" width="100%"/>
      </a>
    </td>
    <td>
      <a href="https://ibb.co/fzH4fBX1">
        <img src="https://i.ibb.co/mV46k1RD/screenshot-2026-05-06-02-42-52.png" alt="screenshot-2" width="100%"/>
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://ibb.co/YByjBfcq">
        <img src="https://i.ibb.co/m5Xz5h9M/screenshot-2026-05-06-02-44-07.png" alt="screenshot-3" width="100%"/>
      </a>
    </td>
    <td>
      <a href="https://ibb.co/7tmZzhtZ">
        <img src="https://i.ibb.co/Ld7cPKdc/screenshot-2026-05-06-02-51-13.png" alt="screenshot-4" width="100%"/>
      </a>
    </td>
  </tr>
</table>

---

## Features

- Smooth player movement (run, jump, gravity)  
- Animated character states (idle, run, jump, fall)  
- Tile-based level design using TMX (Tiled)  
- Key collection and door unlocking system  
- Moving platforms  
- Hazard zones (instant death areas)  
- Trigger-based on-screen messages  
- Modular and organized codebase  

---

## Tech Stack

- Python 3.13.9  
- Pygame  
- pytmx  

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pygame-platformer.git
cd pygame-platformer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**

  ```
  venv\Scripts\activate
  ```

- **Linux / macOS**

  ```
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```

---

## Controls

- Left / Right Arrow — Move  
- Up Arrow / Space — Jump  
- Objective: Collect the key, unlock the door, and reach the exit while avoiding hazards  

---

## Contributing

Contributions are welcome. If you would like to improve the project, feel free to fork the repository and submit a pull request.

1. Fork the repository  
2. Create a new branch (`feature/your-feature-name`)  
3. Commit your changes  
4. Push to your branch  
5. Open a pull request  

---

## License

This project is licensed under the MIT License.

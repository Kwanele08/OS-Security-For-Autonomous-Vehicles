# Secure IPC Simulation for Autonomous Vehicles

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)

A Python-based simulation demonstrating secure Inter-Process Communication (IPC) relevant to autonomous vehicle (AV) internal software modules, focusing on confidentiality, integrity, and authenticity using cryptographic techniques.

## Table of Contents

*   [Overview](#overview)
*   [Problem Statement](#problem-statement)
*   [Features](#features)
*   [Technology Stack](#technology-stack)
*   [Flow Diagram](#flow-diagram)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
*   [Usage](#usage)
*   [Testing Tampering](#testing-tampering)
*   [Limitations](#limitations)
*   [Future Work](#future-work)
*   [Project Report](#project-report)

## Overview

This project simulates secure message passing between two processes, representing hypothetical modules within an autonomous vehicle's operating system (e.g., a perception module sending data to a planning module). It implements cryptographic measures (AES encryption, HMAC authentication) to protect the communication channel against local eavesdropping and message tampering, without relying on hardware dependencies. The goal is to demonstrate fundamental software security principles applicable to safety-critical systems.

## Problem Statement

Autonomous vehicles require secure internal communication between software modules (like perception, planning, control) to prevent eavesdropping or tampering that could lead to unsafe operation. This project addresses the need to design a code-based simulation demonstrating secure Inter-Process Communication (IPC) focusing on confidentiality, integrity, and authenticity without hardware dependencies, suitable for a student project with minimal resources.

## Features

*   **Secure Inter-Process Communication:** Uses ZeroMQ (Push/Pull pattern) for message passing between sender and receiver processes.
*   **Confidentiality:** Encrypts message payloads using AES-256 in CBC mode.
*   **Integrity & Authenticity:** Employs HMAC-SHA256 (using an Encrypt-then-MAC scheme) to detect message tampering and verify the sender's authenticity based on a shared secret.
*   **Tamper Detection:** Demonstrates that modifications to messages during transit are detected and rejected by the receiver.
*   **Modular Design:** Code is organized into sender, receiver, and common utility modules.

## Technology Stack

*   **Language:** Python 3.x
*   **Libraries:**
    *   `pyzmq`: For ZeroMQ messaging (IPC).
    *   `cryptography`: For AES encryption and HMAC-SHA256 implementation.
    *   `json`: For message serialization/deserialization.
*   **Tools:**
    *   Git & GitHub: For version control.
    *   Bash: For the simple execution script (`build.sh`).
    *   (Developed/Tested using GitHub Codespaces).

## Flow Diagram

The following diagram illustrates the message flow and security steps:

```mermaid
graph TD
    subgraph sender_process ["Sender Process (sender.py)"]
        S_Start([Start Sender]) --> S_GetData[Get Data Payload];
        S_GetData --> S_SerPayload[Serialize Payload];
        S_SerPayload --> S_Encrypt[Encrypt Payload AES-256-CBC];
        S_Encrypt --> S_GenMAC[Generate HMAC-SHA256];
        S_GenMAC --> S_Package[Package Final Message];
        S_Package --> S_SerMsg[Serialize Final Message];
        S_SerMsg --> S_Send[Send via ZMQ PUSH];
        S_Send --> S_End([End Sender]);
    end

    subgraph receiver_process ["Receiver Process (receiver.py)"]
        R_Start([Start Receiver]) --> R_Bind[Bind ZMQ PULL Socket];
        R_Bind --> R_Receive[Receive Message Bytes];
        R_Receive --> R_DeserMsg[Deserialize Outer Message];
        R_DeserMsg --> R_Extract[Extract Ciphertext & MAC];
        R_Extract --> R_VerifyMAC{Verify MAC?};
        R_VerifyMAC -- MAC OK --> R_Decrypt[Decrypt Ciphertext AES-256-CBC];
        R_VerifyMAC -- MAC Invalid --> R_Error[Log Error & Discard];
        R_Error --> R_End([End Receiver Cycle]);
        R_Decrypt --> R_DeserPayload[Deserialize Decrypted Payload];
        R_DeserPayload --> R_Process[Process Authentic Data];
        R_Process --> R_End;
    end

    S_Send -- ZeroMQ Transport --> R_Receive;

    classDef decision fill:#f9f,stroke:#333,stroke-width:2px;
    class R_VerifyMAC decision;


git clone https://github.com/Kwanele08/OS-Security-For-Autonomous-Vehicles 
cd OS-Security-For-Autonomous-Vehicles

python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# requirements.txt
pyzmq
cryptography

pip install -r requirements.txt

chmod +x build.sh

./build.sh

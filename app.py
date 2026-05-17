from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
# A secret key is required to use sessions. Keep this secret!
app.secret_key = "my_super_secret_hacker_patootie_key" 

# --- THE SECRET LOGIN PAGE ---
@app.route("/admin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        
        # --- NEW: Print what Python actually sees to your terminal! ---
        print(f"!!! DEBUG: Python saw the password as: '{password}' !!!")
        
        if password == "easy_mode(4upatootie)":
            session["is_vip"] = True
            return redirect("/") 
            
    return render_template("login.html")

# --- DEACTIVATE VIP MODE (LOGOUT) ---
@app.route("/logout")
def logout():
    # This snipps off the VIP wristband and throws it in the trash
    session.pop("is_vip", None) 
    
    # Send them back to the start as a normal player
    return redirect("/")

# --- THE ENTRANCE ---
@app.route("/")
def home():
    return render_template("index.html")

# --- STAGE 1: The Minefield ---
@app.route("/stage-1")
def stage_1():
    # Check if they have the VIP wristband. If not, default to False.
    vip_status = session.get("is_vip", False)
    
    # Send the wristband status to the HTML file
    return render_template("stage1.html", is_vip=vip_status)

# --- STAGE 2: The Gatekeeper ---
@app.route("/stage-2", methods=["GET", "POST"])
def stage_2():
    error_message = None 
    vip_status = session.get("is_vip", False) 

    if request.method == "POST":
        user_guess = request.form.get("answer", "").strip().lower()
        
        # --- NEW: Branching Logic based on VIP status ---
        if vip_status == True:
            # VIPs only need to answer the easy riddle
            if user_guess == "anniversary":
                return redirect("/stage-3")
            else:
                error_message = "CRITICAL ERROR: PASSKEY REJECTED."
        
        else:
            # Normal users must answer the hard riddle
            if user_guess in ["localhost", "127.0.0.1"]:
                return redirect("/stage-3")
            else:
                error_message = "CRITICAL ERROR: PASSKEY REJECTED."

    return render_template("stage2.html", error=error_message, is_vip=vip_status)

# --- STAGE 3: The Hacker ---
@app.route("/stage-3", methods=["GET", "POST"])
def stage_3():
    error_message = None
    vip_status = session.get("is_vip", False)

    if request.method == "POST":
        # Grab the passkey
        user_guess = request.form.get("passkey", "").strip().lower()
        
        # The secret password is "omega_protocol"
        if user_guess == "omega_protocol":
            return redirect("/stage-4")
        else:
            error_message = "ACCESS DENIED: INVALID OVERRIDE KEY."

    return render_template("stage3.html", error=error_message, is_vip=vip_status)

# --- STAGE 4: The URL Manipulator ---
@app.route("/stage-4")
def stage_4():
    vip_status = session.get("is_vip", False)
    
    # Python checks the URL for ?override=true
    override_param = request.args.get("override", "").lower()
    
    if override_param == "true":
        # SUCCESS: We hand them a hidden security token in their browser session
        session["cleared_stage_4"] = True
        return redirect("/stage-5")
        
    return render_template("stage4.html", is_vip=vip_status)


# --- STAGE 5: The Final Win Screen ---
@app.route("/stage-5")
def stage_5():
    # SECURITY CHECK: Did they actually clear stage 4?
    has_token = session.get("cleared_stage_4", False)
    vip_status = session.get("is_vip", False)
    
    if not has_token:
        # Kicked to the cheater dungeon if they tried to skip ahead
        return render_template("cheat_trap.html")
        
    # If they passed honestly, show the glorious victory page!
    return render_template("stage5.html", is_vip=vip_status)

if __name__ == "__main__":
    app.run(debug=True)
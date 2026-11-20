import { useState } from "react";
import { useNavigate, Navigate } from 'react-router';

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";

import getEnvData from "../config";



function LoginPage() {
    /*

    */

    // ============================== STATES ============================== //
    const settings = getEnvData();
    const BACKEND_API_URL = settings.BACKEND_API_URL;
    const LS_SESSION = settings.LS_SESSION;
    
    // ============================== STATES ============================== //
    const [userLogin, setUserLogin] = useState({});
    const [showPassword, setShowPassword] = useState(false);
    
    // ============================== ============================== //
    const navigate = useNavigate();
    const loginFormStructures = [
        {
            format: "input",
            attributes : {
                id: "identity",
                type: "text",
                title: "Votre identifiant",
                value: userLogin.identity || '',
                required: true,
                onChange: (e) => setUserLogin({ ...userLogin, identity: e.target.value }),
            },
            text:"Identifiant"
        },
        {
            format: "input",
            attributes : {
                id: "password",
                type: !showPassword ? "password" : "text",
                title: "Votre mot de passe",
                required: true,
                onChange: (e) => setUserLogin({ ...userLogin, password: e.target.value }),
            },
            text:"Mot de passe"
        },
        {
            format: "checkbox",
            attributes : {
                id: "toggle-show-password",
                value: showPassword,
                onChange: () => setShowPassword(!showPassword),
            },
            text:"Afficher le mot de passe"
        },
        {
            format: "submit",
            attributes: {
                title: "Se connecter",
            },
            text: "Se connecter"
        }
    ];
    

    // ================================ HANDLE SUBMIT ================================ //
    async function signIn(event) {
        /*
        
        */

        event.preventDefault();
        const response = await fetch(
            `${BACKEND_API_URL}/api/v1/login`,
            {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify(userLogin)
            }
        )

        if(response.ok) {
            let data = await response.json();

            if(data.success) {
                localStorage.setItem(LS_SESSION, data.response.sid);
                navigate("/dashboard/id", { replace: true });
            }
        }
    }


    return (
        <> 
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Se connecter à Task Manager
                </CustomH2MediumTitle>
                <FormLayout fields={loginFormStructures}
                            onSubmit={signIn} />
                <AccountOption linkOption={
                    {
                        "href": '/forgot-password',
                        "text": "Mot de passe oublié"
                    }
                } >
                </AccountOption>
                <AccountOption linkOption={
                    {
                        "href": '/register/me',
                        "text": "Créér un compte"
                    }
                } >
                    Vous n'avez pas encore de compte ?
                </AccountOption>
            </BodyLayout>

            <FooterLayout />

        </>
    );
}


export default LoginPage;
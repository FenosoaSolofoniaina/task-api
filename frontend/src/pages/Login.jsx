import { useState } from "react";

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";



function LoginPage() {
    /*

    */

    const [identity, setIdentity] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const loginFormStructures = [
        {
            format: "input",
            attributes : {
                id: "identity",
                type: "text",
                title: "Votre identifiant",
                value: identity,
                required: true,
                onChange: (e) => setIdentity(e.target.value),
            },
            text:"Identifiant *"
        },
        {
            format: "input",
            attributes : {
                id: "password",
                type: !showPassword ? "password" : "text",
                title: "Votre mot de passe",
                required: true,
                onChange: (e) => setPassword(e.target.value),
            },
            text:"Mot de passe *"
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
        console.log(`Try to find sign in with identity "${identity}" and password "${password}"`)

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
                        "text": "?"
                    }
                } >
                    Mot de passe oublié
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
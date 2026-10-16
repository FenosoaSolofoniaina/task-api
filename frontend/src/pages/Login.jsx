import { useRef } from "react";

import { CustomBlueLink } from "../components/Ancres";
import { CustomBlueInput } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";
import { CustomH2MediumTitle } from "../components/Titles";



function LoginForm({ loginForms }) {

    return (
        <>
            {
                loginForms.map(loginItem => <CustomBlueInput
                            key={loginItem.id}
                            ref={loginItem.ref}
                            id={loginItem.id}
                            type={loginItem.type}
                            placeholder={loginItem.placeholder}
                            title={loginItem.title} >
                        {loginItem.text}
                    </CustomBlueInput>
                )
            }
        </>
    );
}


function ForgotPassword() {

    const textLink = "Mot de passe oublié ?";

    return (
        <div className="flex flex-row justify-center items-center m-y-[1em]" >
            <CustomBlueLink hrefLink="/forgot-password"
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function CreateNewAccount() {

    const textLink = "Créér un nouveau compte";

    return (
        <div className="flex flex-row justify-center items-center m-y-[1em]" >
            <p>
                Vous n'avez pas encore de compte ?  
            </p>
            <CustomBlueLink hrefLink="/register" 
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function LoginPage() {

    const identityRef = useRef(null);
    const passwordRef = useRef(null);

    function sendLoginForm(event) {
        event.preventDefault();
        event.stopPropagation();

        console.log("Formulaire envoyée :");
        console.log(`Identifiant : ${identityRef.current.value}`);
        console.log(`Mot de passe : ${passwordRef.current.value}`);

    }

    const loginFormStructures = [
        {
            "id": "identity",
            "ref": identityRef,
            "type": "text",
            "placeholder": "",
            "title": "Identifiant",
            "text": "Identifiant"
        },
        {
            "id": "password",
            "ref": passwordRef,
            "type": "password",
            "placeholder": "",
            "title": "Mot de passe",
            "text": "Mot de passe"
        },
    ];


    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                <CustomH2MediumTitle>
                    Se connecter à Task Manager App
                    </CustomH2MediumTitle>
                <form method="POST"
                      onSubmit={sendLoginForm} >
                    <LoginForm loginForms={loginFormStructures} />
                    <CustomBlueSubmitButton>
                        Se connecter
                    </CustomBlueSubmitButton>
                </form>
                <ForgotPassword />
                <CreateNewAccount />
            </div>
        </div>
    );
}


export default LoginPage; 
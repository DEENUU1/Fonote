"use client";
import React, {useState} from "react";
import Link from "next/link";
import {Button} from "@chakra-ui/react";
import {signIn, useSession} from "next-auth/react";



function Navbar() {
  const {data: session, status} = useSession();

	const [isOpen, setIsOpen] = useState(false);

	const toggleNavbar = () => {
		setIsOpen(!isOpen);
	};

	let navLinks;

    if (status === "loading") {
        navLinks = <p>Loading...</p>;
    } else if (!session) {
        navLinks = (
            <>
                <Link href={"/"} className="px-3 py-2 cursor-pointer font-bold rounded hover:bg-blue-400">
                    Home
                </Link>
                <Link href={"/pricing"} className="px-3 py-2 cursor-pointer rounded hover:bg-blue-400">
                    Pricing
                </Link>
                <Link href={"/contact"} className="px-3 py-2 cursor-pointer rounded hover:bg-blue-400">
                    Contact
                </Link>
                <Button className="px-3 py-2 cursor-pointer rounded font-extrabold hover:bg-blue-400" onClick={() => signIn(undefined, {callbackUrl: "/profile"})}>
                    Login
                </Button>
            </>
        );
    } else {
        navLinks = (
            <>
                <Link href={"/"} className="px-3 py-2 cursor-pointer font-bold rounded hover:bg-blue-400">
                    Home
                </Link>
                <Link href={"/subscription"} className="px-3 py-2 cursor-pointer rounded hover:bg-blue-400">
                    Pricing
                </Link>
                <Link href={"/contact"} className="px-3 py-2 cursor-pointer rounded hover:bg-blue-400">
                    Contact
                </Link>
                <Link href={"/profile"} className="px-3 py-2 cursor-pointer rounded hover:bg-blue-400">
                    Profile
                </Link>
                <Link href={"/dashboard"} className="px-3 py-2 cursor-pointer rounded font-extrabold hover:bg-blue-400">
                    Dashboard
                </Link>
            </>
        );
    }


	return (
		<div className="container relative m-auto p-3 flex justify-between items-center">
			<h1 className="text-2xl font-bold text-blue-600"><a href={"/"}>Fonote</a></h1>
			<nav className={isOpen ? ("flex") : (" hidden md:flex")}>
				<ul
					className={`flex gap-2 ${isOpen ? 'bg-blue-500 text-white' : 'bg-white text-black'} absolute md:relative flex-col md:flex-row w-full shadow md:shadow-none text-center top-12 left-0 md:top-0 md:flex`}>{navLinks}</ul>
			</nav>
			<div className="md:hidden">
				<button className="flex justify-center items-center" onClick={toggleNavbar}>
					<svg
						viewBox="0 0 24 24"
						width="24"
						height="24"
						stroke="currentColor"
						stroke-width="2"
						fill="none"
						stroke-linecap="round"
						stroke-linejoin="round"
						className={isOpen ? ("hidden") : ("flex")}
					>
						<line x1="3" y1="12" x2="21" y2="12"></line>
						<line x1="3" y1="6" x2="21" y2="6"></line>
						<line x1="3" y1="18" x2="21" y2="18"></line>
					</svg>
					<svg
						viewBox="0 0 24 24"
						width="24"
						height="24"
						stroke="currentColor"
						stroke-width="2"
						fill="none"
						stroke-linecap="round"
						stroke-linejoin="round"
						className={isOpen ? ("flex") : ("hidden")}
					>
						<line x1="18" y1="6" x2="6" y2="18"></line>
						<line x1="6" y1="6" x2="18" y2="18"></line>
					</svg>
				</button>
			</div>
		</div>
	);
}

export default Navbar;
import Link from "next/link";


export default function Navbar(){


	return (
		<>
			<nav className="relative px-4 py-4 flex gap-3 items-center bg-white">
				<Link href={"/"}>Home</Link>
				<Link href={"/profile"}>Profile</Link>
				<Link href={"/subscription"}>Pricing</Link>
				<Link href={"/contact"}>Contact</Link>
			</nav>
		</>
	)
}
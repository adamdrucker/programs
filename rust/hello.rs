fn main() {

    // here is my first comment
    println!("Hello!");
    // i have been having weird stomach issues
    println!("I am in need of a doctor");
    /* i will be trying a new doctor soon
    it was a suggestion from someone i know
    i have to make a call to an office tomorrow
    multi line comment */

    // positional arguments
    println!("{0} is the umbrella entity, {1} is the new name for production", "Red Emerald Recordings", "Binary Soul System");

    //named args
    println!("{mind} {body} {soul}",
            mind = "reading + language + work,",
            body = "exercise,",
            soul = "meditation + music" 
            );
    // Rust even checks to make sure the correct number of arguments are used.
    println!("My name is {0}, {1} {0}", "Bond", "James");
    // FIXME ^ Add the missing argument: "James"


    #[allow(dead_code)] // disable `dead_code` which warn against unused module
    struct Structure(i32);
    // This will not compile because `Structure` does not implement
    // fmt::Display.
    // println!("This struct `{}` won't print...", Structure(3));
    // TODO ^ Try uncommenting this line

    let pi = 3.141592;
    println!("Pi is roughly {pi:.*}", 3) 
}

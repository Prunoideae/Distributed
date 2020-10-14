extern crate tokio;

use pyo3::prelude::*;
use pyo3::types::*;
use tokio::net::TcpListener;
use tokio::prelude::*;
use std::io;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>>{
    let gil = Python::acquire_gil();
    let py = gil.python();

    let locals = PyDict::new(py);
    locals.set_item("os", py.import("os").unwrap()).unwrap();
    py.run("os=None", None, Some(&locals)).unwrap();
    println!("{}", locals.get_item("os").unwrap().str().unwrap());
    Ok(())
}

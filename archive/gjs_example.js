#!/usr/bin/gjs

imports.gi.versions.Gtk = '3.0';
const GIRepository = imports.gi.GIRepository;
GIRepository.Repository.prepend_search_path("/usr/lib/gnome-shell");
GIRepository.Repository.prepend_library_path("/usr/lib/gnome-shell");
GIRepository.Repository.prepend_search_path("/usr/lib64/gnome-shell");
GIRepository.Repository.prepend_library_path("/usr/lib64/gnome-shell");

const {GObject, Gtk} = imports.gi;
const Gvc = imports.gi.Gvc;
const Lang = imports.lang;

Gtk.init(null);


// does not work.
// toggling the mic does not trigger the callback
const MyWindow = GObject.registerClass(class MyWindow extends Gtk.Window {
    _init() {
        super._init({ title: "Hello World" });
        this.button = new Gtk.Button({ label: "Click here" });
        this.button.connect("clicked", MyWindow.onButtonClicked);
        this.add(this.button);

        this.mixer_control = new Gvc.MixerControl({name: 'something'});
        this.mixer_control.open()
        print(this.mixer_control)
        this.mixer_control.connect('state_changed', MyWindow._sayHi);
        this.mixer_control.connect('default_source_changed', MyWindow._sayHi);
        this.mixer_control.connect('default-sink-changed', MyWindow._sayHi);
        this.mixer_control.connect('stream-added', MyWindow._sayHi);
        this.mixer_control.connect('stream-removed', MyWindow._sayHi);
        print(this.mixer_control.get_sources());
        print(this.mixer_control.get_source_outputs())
        print(this.mixer_control.get_state())
        print(this.mixer_control.get_default_source())

    }

    static onButtonClicked() {
        print("Hello World");
    }

    static _sayHi() {
        print("hii")
    }
});

let a = new Gvc.MixerControl({name: 'something'});
a.open();

let win = new MyWindow();
win.connect("delete-event", () => Gtk.main_quit());
win.show_all();
Gtk.main();
